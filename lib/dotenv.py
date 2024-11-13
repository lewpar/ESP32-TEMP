class DotEnv:
    _env_vars = {}

    @staticmethod
    def file_exists(path) -> bool:
        try:
            with open(path, "r"):
                return True
        except FileNotFoundError:
            return False

    @staticmethod
    def load(path):
        path = f"{path}/.env"

        if not DotEnv.file_exists(path):
            return

        with open(path, "r") as file:
            lines = file.readlines()
            DotEnv._enumerate_and_set_variables(lines)

    @staticmethod
    def _enumerate_and_set_variables(vars):
        for line in vars:
            sections = line.split('=', 1)
            if len(sections) < 2:
                continue

            key, value = sections[0].strip(), sections[1].strip()
            DotEnv._env_vars[key] = value  # Store in the internal dictionary

    @staticmethod
    def ensure(environment_variable):
        if environment_variable not in DotEnv._env_vars:
            raise Exception(f"Environment variable '{environment_variable}' is required but it was not found.")

    @staticmethod
    def get(variable) -> str:
        if variable not in DotEnv._env_vars:
            raise Exception(f"Environment variable '{variable}' was not found.")

        return DotEnv._env_vars[variable]
