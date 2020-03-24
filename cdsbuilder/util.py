import asyncio
import concurrent.futures
import inspect


def url_path_join(*pieces):
    """Join components of url into a relative url.

    Use to prevent double slash when joining subpath. This will leave the
    initial and final / in place.

    Copied from `notebook.utils.url_path_join`.
    """
    initial = pieces[0].startswith("/")
    final = pieces[-1].endswith("/")
    stripped = [s.strip("/") for s in pieces]
    result = "/".join(s for s in stripped if s)

    if initial:
        result = "/" + result
    if final:
        result = result + "/"
    if result == "//":
        result = "/"

    return result


class DefaultObjDict(dict):
    def __getattr__(self, name):
        if name in self:
            return self[name]
        return None

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)


def maybe_future(obj):
    """Return an asyncio Future

    Use instead of gen.maybe_future

    For our compatibility, this must accept:

    - asyncio coroutine (gen.maybe_future doesn't work in tornado < 5)
    - tornado coroutine (asyncio.ensure_future doesn't work)
    - scalar (asyncio.ensure_future doesn't work)
    - concurrent.futures.Future (asyncio.ensure_future doesn't work)
    - tornado Future (works both ways)
    - asyncio Future (works both ways)
    """
    if inspect.isawaitable(obj):
        # already awaitable, use ensure_future
        return asyncio.ensure_future(obj)
    elif isinstance(obj, concurrent.futures.Future):
        return asyncio.wrap_future(obj)
    else:
        # could also check for tornado.concurrent.Future
        # but with tornado >= 5 tornado.Future is asyncio.Future
        f = asyncio.Future()
        f.set_result(obj)
        return f