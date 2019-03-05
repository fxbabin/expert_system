import argparse
from es_setting import Setting


def main():
    setting = Setting()
    print(setting.rules)
    print(setting.true_facts)
    print(setting.queries)


if __name__ == "__main__":
    main()
