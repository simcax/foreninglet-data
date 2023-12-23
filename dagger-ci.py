"""Execute a command."""

import sys

import anyio
import dagger


async def test():
    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:
        # get reference to the local project
        src = client.host().directory(".")

        python = (
            client.container()
            .from_("python:3.11-slim")
            .with_env_variable("API_USERNAME", "DUMMY")
            .with_env_variable("API_PASSWORD", "DUMMY")
            .with_env_variable("API_BASE_URL", "https://foreninglet.dk/api/")
            .with_env_variable("API_VERSION", "version=1")
            .with_env_variable("API_MEMBERS_API", "members")
            .with_env_variable("API_ACTIVITIES_API", "activities")
            # mount cloned repository into image
            .with_directory("/src", src)
            # set current working directory for next commands
            .with_workdir("/src")
            # Create empty .env file
            .with_new_file(".env")
            # Install main test tools
            .with_exec(["python", "-m", "pip", "install", "poetry", "black", "pylint"])
            # Check standards
            .with_exec(["black", "--check", "."])
            # install test dependencies
            .with_exec(["poetry", "install", "--with", "dev"])
            # run tests
            .with_exec(["poetry", "run", "pytest", "--vcr-record=none", "."])
        )

        # execute
        await python.sync()

    print("Tests succeeded!")


anyio.run(test)
