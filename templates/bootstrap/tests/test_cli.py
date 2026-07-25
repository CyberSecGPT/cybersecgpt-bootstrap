from {{ package_name }}.cli import build_parser


def test_parser_builds() -> None:
    parser = build_parser()
    args = parser.parse_args(["--version"])
    assert args.version is None
