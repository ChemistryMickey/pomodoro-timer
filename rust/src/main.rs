use clap::Parser;
use indicatif::{ProgressBar, ProgressStyle}; // Progress Bar
use rodio::{self, Source};
use std::{thread, time::Duration, time::SystemTime};

const WARNING_MINS: u64 = 5;
const DEFAULT_BEEP_DURATION: u64 = 150;
const WARNING_BEEP_NUM: u64 = 0b11011011;

/// A nifty little CLI pomodoro timer with binary sounds and a progress bar
#[derive(Parser, Debug)]
struct Args {
    /// Duration of the work round [min]
    #[arg(short, long, default_value_t = 30)]
    work: u64,

    /// Duration of the short break round [min]
    #[arg(short, long, default_value_t = 5)]
    short_break: u64,

    /// Duration of the long break round [min]
    #[arg(short, long, default_value_t = 20)]
    long_break: u64,

    /// Number of rounds before the pattern repeats (e.g. [short, short, long, short, short, long, ...])
    #[arg(short, long, default_value_t = 3)]
    rounds_before_long_break: u64,

    /// Produce a series of warning beeps 5 minutes before the work or long break is over
    #[arg(short, long, default_value_t = true)]
    warn: bool,

    /// Skip user input before continuing to the next round (continue without user input)
    #[arg(short = 'i', long, default_value_t = false)]
    skip_input_break: bool,

    /// Don't beep at all. You're missing out though. Learn binary. It'll be fun!
    #[arg(short, long, default_value_t = false)]
    disable_all_sound: bool,
}

fn main() {
    print_banner();
    let parameters: Args = Args::parse();

    if !parameters.skip_input_break {
        wait_for_user_enter("Begin?");
    }
    let mut cur_round: u64 = 1;
    loop {
        work_round(cur_round, &parameters);
        break_round(cur_round, &parameters);

        cur_round += 1;
    }
}

fn work_round(cur_round: u64, parameters: &Args) {
    println!(
        "Starting round {}. Work for {} minutes!",
        cur_round, parameters.work
    );

    if !parameters.disable_all_sound {
        beep_number_in_binary(parameters.work, None);
    }

    wait_with_prog_bar(
        parameters.work,
        WARNING_MINS,
        parameters.warn,
        parameters.disable_all_sound,
        "Work in Progress...",
    );

    println!("Round {cur_round} work complete!");
    if parameters.skip_input_break {
        wait_for_user_enter("Continue to next break?");
    }
}

fn break_round(cur_round: u64, parameters: &Args) {
    let break_mins: u64;
    let break_warning_mins: u64;
    if cur_round % parameters.rounds_before_long_break == 0 {
        break_mins = parameters.long_break;
        break_warning_mins = WARNING_MINS;
    } else {
        break_mins = parameters.short_break;
        break_warning_mins = 0;
    }
    if !parameters.disable_all_sound {
        beep_number_in_binary(break_mins, None);
    }
    println!("Time for a {break_mins} minute break!");

    wait_with_prog_bar(
        break_mins,
        break_warning_mins,
        parameters.warn,
        parameters.disable_all_sound,
        "Break in Progress...",
    );

    println!("Round {cur_round} break complete!");
    if parameters.skip_input_break {
        wait_for_user_enter("Continue to next work round?");
    }
}

// Utils
fn wait_for_user_enter(msg: &str) {
    println!("{}", msg);

    let mut input = String::new();
    std::io::stdin()
        .read_line(&mut input)
        .expect("What? How on earth did you break this?");
}

fn wait_with_prog_bar(
    duration_min: u64,
    warn_mins: u64,
    warn: bool,
    disable_sounds: bool,
    prefix: &str,
) {
    let duration_sec = duration_min * 60;
    let pb: ProgressBar = ProgressBar::new(duration_sec);
    pb.set_style(
        ProgressStyle::with_template(
            format!(
                "{} {{wide_bar:.green/red}} [{{elapsed}}/{}s] ",
                prefix, duration_sec
            )
            .as_str(),
        )
        .unwrap(), // .progress_chars("o|."),
    );
    let mut warn_latch = false;
    for second in 0..duration_sec {
        pb.inc(1);

        let start_time = SystemTime::now();

        if second / 60 == (duration_min - warn_mins) && warn && !warn_latch && !disable_sounds {
            beep_number_in_binary(WARNING_BEEP_NUM, None);
            warn_latch = true;
        }

        let wait_millis = 1000
            - SystemTime::now()
                .duration_since(start_time)
                .unwrap()
                .as_millis();
        thread::sleep(Duration::from_millis(wait_millis as u64));
    }
    pb.finish();

    if !disable_sounds {
        beep_number_in_binary(00000, None);
    }
}

// Sound
fn beep_number_in_binary(num: u64, beep_duration_millis: Option<u64>) {
    // Convert number to binary
    let bin_form: String = format!("{:b}", num);
    let beep_duration_millis = match beep_duration_millis {
        Some(val) => val,
        None => DEFAULT_BEEP_DURATION,
    };
    let low_freq: f32 = 440.0; //A4
    let high_freq: f32 = 659.0; //E5

    let (_stream, stream_handle) = rodio::OutputStream::try_default().unwrap();
    let sink: rodio::Sink = rodio::Sink::try_new(&stream_handle).unwrap();

    // Beep binary representation of number
    for digit in bin_form.as_bytes().iter() {
        let freq: f32;
        if *digit == 49 {
            //ASCII representation of "1" is 49, "0" is 48
            freq = high_freq;
        } else {
            //"0"
            freq = low_freq;
        }
        let source = rodio::source::SineWave::new(freq)
            .take_duration(Duration::from_millis(beep_duration_millis));
        sink.append(source);

        sink.sleep_until_end();
    }
}

// Banner
fn print_banner() {
    let banner: &str = r#"############################################################
#                                                          #
#    ____                           _                 _    #
#   |  _ \ ___  _ __ ___   ___   __| | ___  _ __ ___ | |   #
#   | |_) / _ \| '_ ` _ \ / _ \ / _` |/ _ \| '__/ _ \| |   #
#   |  __/ (_) | | | | | | (_) | (_| | (_) | | | (_) |_|   #
#   |_|   \___/|_| |_| |_|\___/ \__,_|\___/|_|  \___/(_)   #
#                                                          #
#                             +++                          #
#                             -+                           #
#                     +-++   +++ -#   +                    #
#            +    +++++++++++++++++#######                 #
#              ++++++++++--++++++++++-++++###              #
#           ++++++++++++++-+++++##++++##########   +       #
#         +++++++++++++++++++++++####---##########         #
#        ++++++++++++++++++++++++######++++########        #
#       +++++++++++++++++++++++++++#######++++######       #
#      +++++++----++++++++++++++++++#################      #
#     +++++++-----+++++++++++++++++++################      #
#     ++++++++---++++++++++++++++++++#################     #
#    ++++++++++++++++++++++++++++++++#################     #
#    +++++++++-++++++++++++++++++++++#################     #
#    +++++++++++++++++++++++++++++++#################      #
#     +++++++++++++++++++++++++++++##################      #
#     ++++++++++++++++++++++++++++###################      #
#      ++++++++++++++++++++++++++###################       #
#       ++++++++++++++++++++++++###################        #
#        +++++++++++++++++++++####################         #
#         #######+++++++########################           #
#           ##################################             #
#              ############################                #
#                  #####################                   #
#                                                          #
#                                                          #
############################################################
"#;
    println!("{}", banner);
}
