# Use ManimCE's (latest stable) official manim image as a base.
FROM manimcommunity/manim:stable

# Switch to container's root to install system-level packages.
USER root

RUN \
	# Synchronize package list with the remote to prevent 'package not found' errors.
	apt-get update \
	# Install the packages.
	&& apt-get install --assume-yes --no-install-recommends \
#		# Native Wayland / EGL dependencies.
#		libwayland-cursor0 \
#		libwayland-egl1 \
#		# X11 / XWayland dependencies.
#		libxkbcommon0 \
		# Optional: Preview rendered .mp4 files from inside the container.
		mpv \
		xdg-utils \
	# Clean up the package list cache to keep the image size small.
    	&& rm --recursive --force /var/lib/apt/lists/*

# Provide generic symlinks so Python (ModernGL) can find the GL/EGL/GLX runtimes.
# This spares the installation of heavy -dev packages.
RUN ln --symbolic /usr/lib/$(uname --machine)-linux-gnu/libGL.so.1  /usr/lib/$(uname --machine)-linux-gnu/libGL.so  && \
    ln --symbolic /usr/lib/$(uname --machine)-linux-gnu/libEGL.so.1 /usr/lib/$(uname --machine)-linux-gnu/libEGL.so && \
    ln --symbolic /usr/lib/$(uname --machine)-linux-gnu/libGLX.so.0 /usr/lib/$(uname --machine)-linux-gnu/libGLX.so

# Optional: Hijack xdg-open to always use mpv instead.
RUN echo '#!/bin/sh\nmpv "$@"' > /usr/local/bin/xdg-open && \
	chmod +x /usr/local/bin/xdg-open

# Switch to a non-root user for security.
# 'manimuser' is the default user in ManimCE's image.
USER manimuser
