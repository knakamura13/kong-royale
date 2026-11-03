# UI prototyping with Storybook

This is a fork-only prototype on `knakamura/storybook-ui-prototype`; it is not part of upstream `main` and should not be included in upstream PRs unless the maintainers decide to adopt it.

## Run it

```sh
npm ci
npm run storybook
```

Open <http://localhost:6006/>. The first story is the real Learn the controls UI. Use the Controls panel to show or hide its firing-range action. The app remains plain TypeScript and DOM; Storybook only hosts and previews it.

To build a static preview, run `npm run build-storybook`. Generated files go to the ignored `storybook-static/` directory.

## Use it while preparing an upstream UI change

Start the feature branch from `upstream/main` so the upstream PR contains only the feature. While developing a feature branch, test it in a separate worktree based on this Storybook branch and bring the feature commit into that worktree locally. Keep Storybook setup changes out of the upstream feature branch and PR.

Add a story only when it exercises production UI code. Do not recreate a screen just for Storybook; a preview that diverges from the game is not useful evidence.
