"""Z-buffered 3D star rendered as ASCII art (donut.c style)."""

import math
from typing import List


def render_frame(A: float, B: float, width: int = 70, height: int = 35, *,
                 points: int = 5, ring: bool = True, hub: bool = True,
                 chars: str = ".,:;oO0Q@#") -> List[str]:
    """
    Render one frame of a 3D star (spokes, optional ring and hub) as ASCII art.

    Args:
        A: Rotation angle around X-axis
        B: Rotation angle around Y-axis
        width: Output width in characters
        height: Output height in characters
        points: Number of star points (spokes), at least 1
        ring: Draw the outer torus ring
        hub: Draw the centre sphere
        chars: Shading ramp from dim to bright

    Returns:
        List of strings representing the ASCII art frame
    """
    output = [[' ' for _ in range(width)] for _ in range(height)]
    zbuffer = [[0.0 for _ in range(width)] for _ in range(height)]

    if points < 1:
        raise ValueError("points must be at least 1")
    if len(chars) < 4:
        raise ValueError("chars needs at least 4 shading characters")

    cos_A, sin_A = math.cos(A), math.sin(A)
    cos_B, sin_B = math.cos(B), math.sin(B)

    R1 = 0.25  # Thinner ring tube
    R2 = 2.5
    K2 = 5.0
    K1 = width * K2 * 3 / (8 * (R1 + R2))

    theta_step = 0.04
    phi_step = 0.02

    # Torus (outer ring)
    if ring:
        theta = 0.0
        while theta < 2 * math.pi:
            cos_theta = math.cos(theta)
            sin_theta = math.sin(theta)

            phi = 0.0
            while phi < 2 * math.pi:
                cos_phi = math.cos(phi)
                sin_phi = math.sin(phi)

                cx = R2 + R1 * cos_theta
                cy = R1 * sin_theta

                x = cx * cos_phi
                y = cy
                z = cx * sin_phi

                y1 = y * cos_A - z * sin_A
                z1 = y * sin_A + z * cos_A
                x2 = x * cos_B + z1 * sin_B
                z2 = -x * sin_B + z1 * cos_B

                z_screen = K2 + z2
                if z_screen > 0:
                    ooz = 1.0 / z_screen
                    xp = int(width / 2 + K1 * ooz * x2)
                    yp = int(height / 2 - K1 * ooz * y1 * 0.5)

                    nx = cos_theta * cos_phi
                    ny = sin_theta
                    nz = cos_theta * sin_phi

                    ny1 = ny * cos_A - nz * sin_A
                    nz1 = ny * sin_A + nz * cos_A
                    nx2 = nx * cos_B + nz1 * sin_B
                    nz2 = -nx * sin_B + nz1 * cos_B

                    # Lighting with variation across character range
                    L = 0.7 * ny1 + 0.5 * nx2 + 0.4 * nz2
                    # Map from [-1.6, 1.6] to [0.4, 1.0] for dense chars with variation
                    L = 0.4 + abs(L) * 0.4 + max(0, L) * 0.2

                    if 0 <= xp < width and 0 <= yp < height:
                        if ooz > zbuffer[yp][xp]:
                            zbuffer[yp][xp] = ooz
                            lum_idx = int(L * (len(chars) - 1))
                            output[yp][xp] = chars[min(max(0, lum_idx), len(chars) - 1)]

                phi += phi_step
            theta += theta_step

    # Spokes
    spoke_angles = [-math.pi / 2 + 2 * math.pi * k / points for k in range(points)]
    spoke_thickness = 0.12
    spoke_width_hub = 0.18
    spoke_width_tip = 0.06
    hub_r = 0.55
    spoke_end = R2 - 0.35 if ring else R2
    t_step = 0.02
    u_step = 0.1

    for spoke_ang in spoke_angles:
        dx = math.cos(spoke_ang)
        dz = math.sin(spoke_ang)
        px = -dz
        pz = dx

        t = hub_r
        while t <= spoke_end:
            tn = (t - hub_r) / (spoke_end - hub_r)
            curve = 0.12 * math.sin(tn * math.pi)
            w = spoke_width_hub * (1 - tn) + spoke_width_tip * tn

            u = -1.0
            while u <= 1.0:
                for side in (-1, 1):
                    x = dx * t + px * u * w
                    z = dz * t + pz * u * w
                    y = curve + side * spoke_thickness * (1 - abs(u) * 0.7)

                    y1 = y * cos_A - z * sin_A
                    z1 = y * sin_A + z * cos_A
                    x2 = x * cos_B + z1 * sin_B
                    z2 = -x * sin_B + z1 * cos_B

                    z_screen = K2 + z2
                    if z_screen > 0:
                        ooz = 1.0 / z_screen
                        xp = int(width / 2 + K1 * ooz * x2)
                        yp = int(height / 2 - K1 * ooz * y1 * 0.5)

                        ny_local = side
                        ny1 = ny_local * cos_A
                        nz1 = ny_local * sin_A
                        # Spokes lighting - higher base for visibility
                        L = abs(0.8 * ny1 + 0.4 * nz1) + 0.4

                        if 0 <= xp < width and 0 <= yp < height:
                            if ooz > zbuffer[yp][xp]:
                                zbuffer[yp][xp] = ooz
                                lum_idx = int(L * (len(chars) - 1))
                                output[yp][xp] = chars[min(max(3, lum_idx), len(chars) - 1)]

                u += u_step
            t += t_step

    if hub:
        # Hub sphere
        hub_radius = 0.5
        sphere_step = 0.08

        phi = 0.0
        while phi < math.pi:
            cos_phi = math.cos(phi)
            sin_phi = math.sin(phi)

            theta = 0.0
            while theta < 2 * math.pi:
                cos_theta = math.cos(theta)
                sin_theta = math.sin(theta)

                x = hub_radius * sin_phi * cos_theta
                y = hub_radius * sin_phi * sin_theta
                z = hub_radius * cos_phi

                y1 = y * cos_A - z * sin_A
                z1 = y * sin_A + z * cos_A
                x2 = x * cos_B + z1 * sin_B
                z2 = -x * sin_B + z1 * cos_B

                z_screen = K2 + z2
                if z_screen > 0:
                    ooz = 1.0 / z_screen
                    xp = int(width / 2 + K1 * ooz * x2)
                    yp = int(height / 2 - K1 * ooz * y1 * 0.5)

                    nx = sin_phi * cos_theta
                    ny = sin_phi * sin_theta
                    nz = cos_phi

                    ny1 = ny * cos_A - nz * sin_A
                    nz1 = ny * sin_A + nz * cos_A
                    nx2 = nx * cos_B + nz1 * sin_B

                    # Hub lighting - higher base for visibility
                    L = 0.6 * ny1 + 0.5 * nx2 + 0.5

                    if 0 <= xp < width and 0 <= yp < height:
                        if ooz > zbuffer[yp][xp]:
                            zbuffer[yp][xp] = ooz
                            lum_idx = int(L * (len(chars) - 1))
                            output[yp][xp] = chars[min(max(3, lum_idx), len(chars) - 1)]

                theta += sphere_step
            phi += sphere_step

    return [''.join(row) for row in output]
