## Template placeholders

Raw project templates use `{{ placeholder_name }}` as the canonical placeholder
syntax in both file contents and path names. The renderer also accepts the legacy
single-brace form, `{placeholder_name}`, for compatibility. Every placeholder used
by a template must have a non-empty replacement when it is rendered; otherwise
rendering fails with an unresolved-placeholder error. Binary files are copied
unchanged.
