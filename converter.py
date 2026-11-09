import math

# WGS84 reference ellipsoid parameters
WGS84_A = 6378137.0
WGS84_F = 1 / 298.257223563

WGS84_B = WGS84_A * (1 - WGS84_F)
WGS84_E2 = WGS84_F * (2 - WGS84_F)
WGS84_EP2 = (WGS84_A**2 - WGS84_B**2) / WGS84_B**2


def ecef_to_geodetic(x, y, z):
    """
    Convert ECEF Cartesian coordinates to WGS84 geodetic coordinates.

    Parameters:
        x, y, z: ECEF coordinates in metres.

    Returns:
        latitude: degrees
        longitude: degrees
        height: ellipsoidal height in metres
    """

    # Check that coordinates are valid numbers
    if not all(math.isfinite(value) for value in (x, y, z)):
        raise ValueError("Coordinates must be finite numbers.")

    # Distance from the Z-axis
    p = math.hypot(x, y)

    # The centre of the Earth has no defined geodetic coordinates
    if p == 0 and z == 0:
        raise ValueError("Geodetic coordinates are undefined at Earth's centre.")

    # Handle the poles separately
    if p == 0:
        latitude = math.copysign(90.0, z)
        longitude = 0.0
        height = abs(z) - WGS84_B
        return latitude, longitude, height

    # Longitude
    longitude = math.atan2(y, x)

    # Bowring's auxiliary angle
    theta = math.atan2(z * WGS84_A, p * WGS84_B)

    sin_theta = math.sin(theta)
    cos_theta = math.cos(theta)

    # Geodetic latitude
    latitude = math.atan2(
        z + WGS84_EP2 * WGS84_B * sin_theta**3,
        p - WGS84_E2 * WGS84_A * cos_theta**3
    )

    # Radius of curvature in the prime vertical
    sin_latitude = math.sin(latitude)
    N = WGS84_A / math.sqrt(
        1 - WGS84_E2 * sin_latitude**2
    )

    # Ellipsoidal height
    height = p * math.cos(latitude) + z * math.sin(latitude) - (
        WGS84_A**2 / N
    )

    # Convert radians to degrees
    latitude = math.degrees(latitude)
    longitude = math.degrees(longitude)

    return latitude, longitude, height


if __name__ == "__main__":
    print("WGS84 ECEF to Geodetic Coordinate Converter")
    print("-" * 45)

    try:
        x = float(input("Enter X coordinate (metres): "))
        y = float(input("Enter Y coordinate (metres): "))
        z = float(input("Enter Z coordinate (metres): "))

        lat, lon, h = ecef_to_geodetic(x, y, z)

        print("\nGeodetic Coordinates")
        print("-" * 30)
        print(f"Latitude:  {lat:.8f} degrees")
        print(f"Longitude: {lon:.8f} degrees")
        print(f"Height:    {h:.4f} metres")

    except ValueError as error:
        print(f"Error: {error}")
