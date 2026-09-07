# Publication and domain handoff

Target hostname: **braking.fde.guru**. The founder will configure Cloudflare manually later. No DNS changes are performed in this phase.

The private GitHub repository stores source archives and working engineering. Only explicitly selected original reports and research metadata are copied to the website. Third-party PDFs, catalogue images, raw page bodies, confidential supplier documents and the session transcript must not appear in the deployment archive.

The Sites preview initially remains owner-only. To make it publicly accessible later, change the Site audience deliberately. A DNS record does not itself change viewer access.

For a custom domain on Sites: first register the exact hostname with the hosting provider so that it returns the required routing and certificate-validation records. Then add those exact records in your Cloudflare DNS dashboard, following the provider's proxy and TLS instructions. Do not guess the CNAME target or use the visible preview hostname without checking the returned configuration. Verify certificate issuance and routing before announcing the domain.

Alternatively, deploy the reviewed website source through a Cloudflare-supported build flow in your own account, then attach the custom hostname there. Preserve the public-export filter. The current build is a Sites/Vinext Cloudflare Worker application, not an instruction to upload the private repository as static files.

Original future design releases must carry part/revision identifiers, maturity status, limitations and release evidence. Publishing files does not by itself select an open-hardware licence; choose the licence before the first original CAD release. Third-party rights remain with their owners.
