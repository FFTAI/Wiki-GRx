import argparse
from robot_rcs_gr.sdk.server import RobotServer

def main(config: str, freq: int, debug_interval: int, verbose: bool, visualize: bool):
    """
    Main function to initialize and start the RobotServer.

    :param config: Path to the config file.
    :param freq: Main loop frequency in Hz.
    :param debug_interval: Debug loop print interval.
    :param verbose: Flag to print internal debug info.
    :param visualize: Flag to visualize the robot in RViz.
    """
    # If verbose is False, turn off the logger
    if not verbose:
        from robot_rcs.logger.fi_logger import Logger
        Logger().state = Logger().STATE_OFF

    # Initialize the RobotServer with the provided parameters
    robot = RobotServer(config, freq=freq, debug_print_interval=debug_interval, visualize=visualize)
    
    # Start the RobotServer's main loop
    robot.spin()

if __name__ == "__main__":
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Robot server configuration.")
    
    # add argument
    parser.add_argument('config', help="Path to the config file")
    parser.add_argument('--freq', type=int, default=500, help="Main loop frequency in Hz. defaults to 500 Hz.")
    parser.add_argument('--debug_interval', type=int, default=0, help="Debug loop print interval")
    parser.add_argument('--verbose', type=bool, default=True, help="Print internal debug info")
    parser.add_argument('--visualize', type=bool, default=True, help="Visualize the robot in RViz")

    # Parse the arguments
    args = parser.parse_args()

    # Call the main function with the parsed arguments
    main(
        config=args.config,
        freq=args.freq,
        debug_interval=args.debug_interval,
        verbose=args.verbose,
        visualize=args.visualize
    )

