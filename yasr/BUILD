resource(name="version", source="yasr/.version")

python_sources(name="src", sources=["yasr/**/*.py"], dependencies=["3rdparty:reqs"])

python_distribution(
    name="dist",
    dependencies=[
        ":src",
        ":version",
        # Dependencies on code to be packaged into the distribution.
    ],
    provides=python_artifact(
        name="yasr",
    ),
    entry_points={"console_scripts": {"yasr": "yasr:cli.app"}},
    # Example of setuptools config, other build backends may have other config.
    wheel_config_settings={"--global-option": ["--python-tag", "py39"]},
    # Don't use setuptools with a generated setup.py.
    # You can also turn this off globally in pants.toml:
    #
    # [setup-py-generation]
    # generate_setup_default = false
    wheel=True,
    generate_setup=True,
    # repositories=["@codeartifact"]
)
