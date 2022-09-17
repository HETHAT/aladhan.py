# pragma: no cover
import argparse
import json
import platform
import sys
import time

import pkg_resources

import aladhan

try:
    import aiohttp
except ModuleNotFoundError:
    aiohttp = None
try:
    import requests
except ModuleNotFoundError:
    requests = None


def show_version():
    entries = []

    entries.append(
        "- Python v{0.major}.{0.minor}.{0.micro}-{0.releaselevel}".format(
            sys.version_info
        )
    )
    version_info = aladhan.version_info
    entries.append(
        "- aladhan.py v{0.major}.{0.minor}.{0.micro}-{0.releaselevel}".format(
            version_info
        )
    )
    if version_info.releaselevel != "final":
        pkg = pkg_resources.get_distribution("aladhan.py")
        if pkg:
            entries.append(f"    - aladhan.py pkg_resources: v{pkg.version}")

    entries.append(f"- aiohttp v{aiohttp and aiohttp.__version__}")
    entries.append(f"- requests v{requests and requests.__version__}")
    uname = platform.uname()
    entries.append(
        "- system info: {0.system} {0.release} {0.version}".format(uname)
    )
    print("\n".join(entries))


def core(_, args):
    if args.version:
        show_version()


def print_json(res, indent):
    res = json.dumps(res, indent=indent)
    print(res)


def save_json(path, res, indent):
    with open(path, "w") as f:
        json.dump(res, f, indent=indent)
    print(f"saved response to {path}")


def to_date_and_params(params):
    params = dict(params)
    date = params.get("date", "")
    if date:
        params.pop("date")
    return dict(date=date, params=params)


def to_hijri_and_params(params):
    params = dict(params)
    hijri = params.get("hijri")
    params = dict(params=params)
    if hijri.lower() != "false" and hijri:
        params["hijri"] = True
    return params


def to_args(params):
    return dict(params=(i for i, in params))


def to_params(getter: str, params: list):
    if getter.startswith(("timings", "next_prayer")):
        params = to_date_and_params(params)
    elif getter.startswith("calendar"):
        params = to_hijri_and_params(params)
    elif len(params[0]) == 1:
        params = to_args(params)
    else:
        params = dict(params)
    return params


def request(parser, args):
    try:
        func = getattr(aladhan.http.HTTPClient(), "get_" + args.getter, None)
    except ImportError:
        parser.error(
            "`requests` library isn't installed which is required to "
            "use this command."
        )
    if func is None:
        parser.error(
            f"couldn't find a getter with the name of `{args.getter}` "
            "Do `python -m aladhan list` to see all available getters."
        )
    ts_start = time.perf_counter()
    if args.params:
        params = to_params(args.getter, args.params)
        try:
            res = func(**params)
        except aladhan.exceptions.HTTPException as e:
            res = e.response
    else:
        res = func()
    ts_end = time.perf_counter() - ts_start
    if args.file is None:
        print_json(res, args.indent)
    else:
        save_json(args.file, res, args.indent)
    print(f"Taken time: {ts_end * 1000:.2f}ms")


def add_request_args(subparser):
    parser = subparser.add_parser(
        "request",
        help="Command for doing requests to the api",
        usage="%(prog)s [options...] getter [params...]",
    )
    parser.set_defaults(func=request)
    parser.add_argument("getter", action="store", help="Getter's name")
    parser.add_argument(
        "params",
        action="store",
        nargs="*",
        type=lambda kv: kv.split("=", 1),
        help="Parameters that will be passed to the getter.",
    )
    parser.add_argument(
        "-f",
        "--file",
        action="store",
        help="Where to store the json response. "
        "If it wasn't given it will print to console.",
        default=None,
    )
    parser.add_argument(
        "-i",
        "--indent",
        action="store",
        help="Indent format value, passing none -> no indents. (default=4)",
        type=lambda kv: int(kv) if kv.isnumeric() else None,
        default=4,
    )


def list_getters(*_):
    getters = []
    for name in sorted(dir(aladhan.http.HTTPClient)):
        if not name.startswith("get_"):
            continue
        name = name[4:]
        getters.append(f"-- {name}")
    print("\n".join(getters))


def add_list_getters_args(subparser):
    parser = subparser.add_parser(
        "list_getters", help="Lists all available getters", aliases=["lg"]
    )
    parser.set_defaults(func=list_getters)


def parse_args():
    parser = argparse.ArgumentParser(
        prog="aladhan", description="Tools for helping with aladhan.py"
    )
    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="shows the library version",
    )
    parser.set_defaults(func=core)
    subparser = parser.add_subparsers(dest="subcommand", title="subcommands")
    add_request_args(subparser)
    add_list_getters_args(subparser)
    return parser, parser.parse_args()


def main():
    parser, args = parse_args()
    args.func(parser, args)


if __name__ == "__main__":
    main()
