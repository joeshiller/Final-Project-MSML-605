from loguru import logger

from msml605 import config, run


def main():
    cfg = config.load_config(config.config_path)

    a_run = run.create_run(cfg, change_description="A run")

    run_file = run.write_run(a_run, cfg.get_run_dir())
    logger.debug("Wrote to new run file. run_file={}", run_file)


if __name__ == "__main__":
    main()
