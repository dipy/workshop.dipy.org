# Workshop.dipy.org
The DIPY Workshop website

## Background

This site makes use of [Sphinx](https://www.sphinx-doc.org/en/stable/) and was built upon [Bootstrap](https://getbootstrap.com) via [Pydata Sphinx Theme](https://pydata-sphinx-theme.readthedocs.io/en/latest/).

We use Github Webhook to deploy the website and IU server (Indiana University) to host the [website](https://workshop.dipy.org/). The deployment is automatic. As soon as push to main branch happened (via merged Pull Request or direct commit), the webhook is sent to hosting server (IU) which pull the last changes and update the website.

## Index

- `_static`: Contains all assets (images, CSS, JS) for Sphinx to look at.
- `_templates`: Contains html layout for custom Sphinx design.
- `_build`: Contains the generated documentation.
- `sphinxext`: Sphinx custom plugins (Especially multiple custon directive).

## Testing Locally: Doc generation steps:

### Installing requirements

To set up your computer to run this site locally, you need to install the various Python packages in the [requirements.txt](requirements.txt) at the top level of this repository.

```bash
$ pip install -U -r requirements.txt
$ pre-commit run --all-files
```

### Generate all the Documentation

#### Under Linux and OSX

```bash
$ make -C . clean && make -C . html
```

#### Under Windows

```bash
$ ./make.bat clean
$ ./make.bat html
```

This will build a collection of html pages under `_build/html` and you can open the `index.html` using your browser of choice.

## Creating a PR

When you are happy with any changes you have made to the website.
We recommend building the website and making sure that everything is building fine.
You should see no warnings for the build.

Once you are sure everything is in order, you can send a PR to this repository.
If you are unfamiliar with this, please see this guide from [GitHub.](https://help.github.com/articles/about-pull-requests/)

## PR Review

When a PR is opened, Github Action will create a preview of any content or style changes.

This must pass before the PR will be merged, furthermore, one review is required before a PR can be merged as well.
