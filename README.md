django-grunt
============

django-grunt provides settings, management commands, a view mixin and a
template context processor to improve your workflow using Grunt
with Django.

### Motivation

<a href="http://gruntjs.com/" target="_blank">Grunt</a> is great for
managing tasks that manipulate your project's static files. You can
use its plugins to compile LESS or SASS into CSS. You can minify JavaScript
or build production files for use with RequireJS. The possibilities
are limitless if you put in the effort to build your own Grunt plugins.

The problem is that typical Django projects use the staticfiles app for
managing static files. Static files are usually stored in several
locations without a common directory ancestor. Before you can use Grunt
to manipulate your static files, you need to run the `collectstatic` management
command to gather all of your static files into one common directory.

After running Grunt to process your collected static files, you need to change
some settings and use the `runserver` management command to test out the
processed files in your browser.

django-grunt helps to simplify this process with management commands and
template context variables.

### Installation and Usage

django-grunt is available on PyPI, so you should install it with pip:

```
pip install django-grunt
```

To use the management commands, you should add `"grunt"` to
`INSTALLED_APPS` in your settings file.

### Management Commands

django-grunt provides two management commands to simplify your workflow:

#### `manage.py grunt [grunt command ...]`

This command runs Django's `collectstatic` command and then invokes `grunt`
with the given `[grunt command ...]` labels.

If you have a Grunt `build` command set up in your Gruntfile.js configuration,
you can run `manage.py grunt build` to collect your static files into the
`settings.STATIC_ROOT` directory and then run `grunt build` on them.

#### `manage.py gruntserver [runserver argument ...]`

This command configures your project's settings so that `runserver` will
serve the files from `settings.STATIC_ROOT` and then invokes `runserver`.

It also configures some settings values that you can pass to your templates
with the provided view mixin or context processor. These values can be used by
your templates to decide which CSS and JavaScript sources to load.

The command also turns on Django's `GZipMiddleware` so that you can simulate
a proper gzip setup on your production server. This can help you get an
accurate feel for your project's static files payload in a production
environment.

### Template context variables and settings

django-grunt provides a view mixin and context processor that you can use
to pass Grunt-related context variables to your templates. Both methods
set boolean values named `grunt_js` and `grunt_css`, which your templates can
use to decide whether to serve "normal" static files or static files which
have been processed by Grunt. These values are `False` by default. Generally,
they'll be `False` in development and `True` in your production server's
settings file. The `gruntserver` management command sets them to `True` so you
can simulate your production setup.

The view mixin is located in `grunt.views.mixins.GruntConfigMixin`. You
should call its `grunt_config()` method to retrieve or update a dictionary
of context variables. It accepts an optional dictionary to update in the
`config` parameter.

If your project uses class-based views, a useful pattern is to override
Django's generic views with additional mixins that provide global configuration
data to all of your templates. As an example, suppose you have a `core`
application in your project and that it defines generic view overrides.
Your `core.views` module can provide its own `TemplateView` using the
`GruntConfigMixin` like so:

```python
from django.views import generic

from grunt.views.mixins import GruntConfigMixin


class ConfigMixin(GruntConfigMixin, generic.base.ContextMixin):
    """
    Global configuration context mixin for all generic views.
    
    """
    def get_context_data(self, **context):
        return self.grunt_config(
            super(ConfigMixin, self).get_context_data(**context))


class TemplateView(ConfigMixin, generic.TemplateView):
    pass
```

Now, rather than inheriting from `django.views.generic.TemplateView`, your
project's views should inherit from `core.views.TemplateView`, and they'll
automatically pass the `grunt_js` and `grunt_css` context variables to your
templates.

Note that `django.views.generic.base.ContextMixin` is only available in
Django 1.5+, so you'll need to make some adjustments for older versions of
Django. The refactor of the generic view `get_context_data()` method into
its own mixin base class was a great change, because it allows you to set
up mixin classes like this that safely call `super()` and simply need to be
inherited to override generic view functionality.

If you're not using class-based views, or you're not ready to commit to
providing your own generic view class overrides, you can alternatively
add `"grunt.context_processors.grunt_config"` to
`TEMPLATE_CONTEXT_PROCESSORS` in your settings file. This will add the
`grunt_js` and `grunt_css` boolean values to all of your templates whose
views use a `RequestContext`.

For both the mixin and the context processor, you can nest the `grunt_js`
and `grunt_css` context variables under a key in the context dictionary.
For the mixin, pass a `key` argument to the `grunt_config()` call. For
the context processor, add a `GRUNT_TEMPLATE_CONTEXT_KEY` to your settings
file.

### Notes and other considerations

I built this project to improve my workflow with Django and Grunt.
I work in a *nix environment, so I didn't bother with trying to support
other platforms.

The `grunt` management command checks for the availability of Grunt on the
command line by running the *nix command `which grunt`. This will fail
on other platforms. I wasn't satisfied with the various cross-platform 
hacks for this problem that I found with a cursory Web search, so
this Django application is only useful on *nix platforms for now.

The management commands were implemented by extending Django's command
API with more declarative features. Since the `grunt` and `gruntserver`
commands need to run other management commands, I built the API to
easily accommodate multiple option groups and actions to perform. If
you are writing complex management commands, the work here may help you
get started. See `grunt.management.base` and `grunt.management.standard`
to see my approach to this problem.

This project currently lacks tests. I'm not feeling particularly motivated
to figure out a decent way to test the management commands. The code is
pretty straightforward and succinct, but it would be better with some
test coverage.

When I have some more time, I'm hoping to add tools to seamlessly integrate
Grunt unit testing tools with Django. However, my goal is to keep the
project as generic as possible, so that it's not tied to any specific
Grunt plugins.

Pull requests are always welcome if you have ideas to fix this project's
shortcomings or add new, useful features. Happy coding!
