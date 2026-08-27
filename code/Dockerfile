# BUILD manim-sandbox
# > A Docker image meant for rendering and displaying Manim code utilizing GPU acceleration
# > regardless of display protocol (X11 or Wayland) and the host machine's GPU make.

# Use ManimCE's (latest stable) official manim image as a base.
FROM manimcommunity/manim:stable

# Switch to container's root to install system-level packages.
USER root

RUN \
    # Synchronize package list with the remote to prevent 'package not found' errors.
    apt-get update \
    # Install the packages.
    && apt-get install --assume-yes --no-install-recommends \
        # Preview rendered .mp4 files from inside the container.
        mpv \
    # Clean up the package list cache to keep the image size small.
    && rm --recursive --force /var/lib/apt/lists/*

# Restore config-file precedence for the renderer.
# ManimCE declares '--renderer' with default="cairo", while every comparable flag
# (--force_window, --write_to_movie, --preview, ...) uses default=None so that an unpassed
# flag defers to manim.cfg. Because this one default is concrete, digest_args() overwrites
# the config value on every single invocation and 'renderer = opengl' in manim.cfg is
# silently ignored. Flipping the default back to None makes manim.cfg authoritative;
# an explicit --renderer on the command line still wins. The assert fails the build loudly if
# a base-image bump moves the target, rather than quietly dropping us back onto the Cairo renderer.
RUN python -c 'import manim.cli.render.render_options as o; p = o.__file__; s = open(p).read(); old = "default=\"cairo\","; assert s.count(old) == 1, p; open(p, "w").write(s.replace(old, "default=None,"))'

RUN set -eux; \
    # Provide generic symlinks so Python (ModernGL) can find the GL/EGL/GLX runtimes.
    # This spares the installation of heavy -dev packages.
    libdir="/usr/lib/$(uname --machine)-linux-gnu"; \
    ln --symbolic "${libdir}/libGL.so.1"  "${libdir}/libGL.so"; \
    ln --symbolic "${libdir}/libEGL.so.1" "${libdir}/libEGL.so"; \
    ln --symbolic "${libdir}/libGLX.so.0" "${libdir}/libGLX.so"; \
    # Hijack xdg-open, which is what Manim's --preview shells out to, so that it always
    # hands the file to mpv. /usr/local/bin precedes /usr/bin on PATH, so this wins.
    printf '%s\n' '#!/bin/sh' 'exec mpv "$@"' > /usr/local/bin/xdg-open; \
    chmod +x /usr/local/bin/xdg-open

# Switch to a non-root user for security.
# 'manimuser' is the default user in ManimCE's image.
USER manimuser
