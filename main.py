from github import Github
import os
import re


def get_env_var(env_var_name, echo_value=False):
    """Try to get the value from a environmental variable.
    If the values is 'None', then a ValueError exception will
    be thrown.
    Args
    ----
        env_var_name : str
            The name of the environmental variable.
        echo_value : bool
            Print the resulting value.
    Returns
    -------
        value : str
            The value from the environmental variable.
    """
    value = os.environ.get(env_var_name)

    if value is None:
        raise ValueError(f"The environmental variable {env_var_name} is empty!")

    if echo_value:
        print(f"{env_var_name} = {value}")

    return value


def main():
    github_token = get_env_var("INPUT_GITHUB_TOKEN")
    pr_number = get_env_var("INPUT_PR_NUMBER")

    # Get needed values from the environmental variables
    repo_name = get_env_var("GITHUB_REPOSITORY")
    github_ref = get_env_var("GITHUB_REF")
    github_event_name = get_env_var("GITHUB_EVENT_NAME")

    # Create a repository object, using the GitHub token
    repo = Github(github_token).get_repo(repo_name)

    # When this actions runs on a "pull_request_target" event, the pull request number is not
    # available in the environmental variables; in that case it must be defined as an input
    # value. Otherwise, we will extract it from the 'GITHUB_REF' variable.
    if github_event_name == 'pull_request_target':
        # Verify the passed pull request number
        try:
            pr_number=int(pr_number)
        except ValueError:
            print(f'A valid pull request number input must be defined when triggering on ' \
                f'"pull_request_target". The pull request number passed was "{pr_number_str}".')
            raise
    else:
        # Try to extract the pull request number from the GitHub reference.
        try:
            pr_number=int(re.search('refs/pull/([0-9]+)/merge', github_ref).group(1))
        except AttributeError:
            print(f'The pull request number could not be extracted from the GITHUB_REF = ' \
                f'"{github_ref}"')
            raise

    print(f'Pull request number: {pr_number}')

    # Create a pull request object
    pr = repo.get_pull(pr_number)
    # Retrieve labels from pull request
    labels = [label.name for label in pr.get_labels()]
    my_output = f"{labels}"

    print(f"::set-output name=prLabels::{my_output}")


if __name__ == "__main__":
    main()
