"""Execute a command."""

import sys

import anyio
import dagger


async def test():
    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:
        # get reference to the local project
        src = client.host().directory(
            ".", exclude=[".git", ".venv", ".venvdagger", "dist", "junit"]
        )

        python = (
            client.container()
            .from_("python:3.13-slim")
            # Install uv
            .with_exec(
                [
                    "python",
                    "-m",
                    "pip",
                    "install",
                    "uv",
                ]
            )
            # mount cloned repository into image
            .with_directory("/src", src)
            # set current working directory for next commands
            .with_workdir("/src")
            # install dependencies with uv
            .with_exec(["uv", "sync"])
            .with_env_variable("API_USERNAME", "DUMMY")
            .with_env_variable("API_PASSWORD", "DUMMY")
            .with_env_variable("API_BASE_URL", "https://foreninglet.dk/api/")
            .with_env_variable("API_VERSION", "version=1")
            .with_env_variable("API_MEMBERS_API", "members")
            .with_env_variable("API_ACTIVITIES_API", "activities")
            .with_env_variable("API_RESIGNED_MEMBERS_API", "members/status/resigned")
            .with_env_variable("MEMBERSHIP_KEYWORDS", "medlemskab,medlemsskab")
            .with_env_variable("TEST_ENVIRONMENT", "True")
            # Check standards
            .with_exec(
                [
                    "uv",
                    "run",
                    "black",
                    "--check",
                    "--diff",
                    "--color",
                    "--exclude",
                    "(.venv|foreninglet_data/sdk/)",
                    ".",
                ]
            )
            # run tests
            .with_exec(
                [
                    "uv",
                    "run",
                    "pytest",
                    "--vcr-record=none",
                    "tests/",
                    "--junitxml=junit/test-results.xml",
                    "--cov=foreninglet_data",
                    "--cov-report=xml",
                    "--cov-report=html",
                ]
            )
        )

        # execute
        await python.sync()

    print("Tests succeeded!")


anyio.run(test)
