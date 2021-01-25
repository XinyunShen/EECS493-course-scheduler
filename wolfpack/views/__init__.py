"""Views, one for each wolfpack page."""
from wolfpack.views.index import show_index
from wolfpack.views.user import show_user_slug
from wolfpack.views.user import show_user_following
from wolfpack.views.user import show_user_followers
from wolfpack.views.accounts import login
from wolfpack.views.accounts import logout
from wolfpack.views.accounts import edit
from wolfpack.views.explore import show_explore
