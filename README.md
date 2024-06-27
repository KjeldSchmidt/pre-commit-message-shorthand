## A pre-commit hook for reduced overhead in writing commit messages.

This plugin allows you to write commit messages like this:

```
Foo the bar to baz the bat

#jira/4567

:robert
```

and have them turn into this:

```
Foo the bar to baz the bat

https://acme.atlassian.net/browse/project-4567

Co-authored-by: Robert Person <robert.person@acme.com>
```

This is achieved through simple string replacement, fully configured in your 
pre-commit configuration. There are no default substitutions.

The rules for substitution are configured as a JSON-dictionary. To use this hook,
add the following to your `.pre-commit-config.yaml`. 🚨Note the first line - 
**it won't work without adding `commit-msg` to the `default_install_hook_types`
property.** 🚨

```yaml
default_install_hook_types: [pre-commit, commit-msg]

repos:
  - repo: https://github.com/KjeldSchmidt/pre-commit-message-shorthand
    rev: v1.0.0
    hooks:
      - id: message-shorthand
        verbose: true
        args:
          - >
            {
              "#jira/": "https://acme.atlassian.net/browse/project-",
              ":robert": "Co-authored-by: Robert Person <robert@person.com>"
            }
```
