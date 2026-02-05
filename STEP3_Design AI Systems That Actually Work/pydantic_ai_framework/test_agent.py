from dataclasses import dataclass

@dataclass
class MovieContext:
    valid_movies: list[str]

class RunContext():
    def __init__(self, deps: MovieContext):
        self.deps = deps

def verify_movie(ctx: RunContext, name: str):
    """Unit testing"""
    for movie in ctx.deps.valid_movies:
        if movie.lower() == name.lower():
            return f"{movie} movie found"

    return f"{name} movie not found"

context = MovieContext(valid_movies=["The Last of Us", "The Witcher", "The Matrix", "The Dark Knight"])
run_context = RunContext(context)

result = verify_movie(run_context, "the witcher")
assert result == "The Witcher movie found"