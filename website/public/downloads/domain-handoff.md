# Cloudflare Workers deployment

The connected Cloudflare project is a Worker named `ai-braking` (not a Pages static export). Keep root directory `/` and deploy command `npx wrangler deploy`.

The root package installs the pinned website dependencies and builds the app in its postinstall step. This supports the currently configured pipeline, which has no separate build command. An optional explicit build command is `npm run build`; it is redundant after a normal install. Do not disable npm lifecycle scripts or dependency installation.

Root `wrangler.jsonc` deploys the generated server modules from `website/dist/server` with public assets from `website/dist/client`. Source archives are not uploaded as website assets. The small original handbook PDF is ordinary Git content so CI does not need Git LFS to serve it; reference archives remain stored using Git LFS in the public repository.

Local verification: `npm ci`, then `npx wrangler deploy --dry-run`. No Cloudflare credentials are needed for the dry run. Do not point static assets at the repository root, which contains research archives and server source.

The domain braking.fde.guru is already attached by the owner. This change does not alter DNS or domain routing. A successful build and a live content check are required before declaring deployment complete.
