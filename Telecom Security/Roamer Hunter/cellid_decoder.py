import sys

def decode_cgid(hex_string):
    # Normalize input
    hex_string = hex_string.lower().replace(" ", "").replace("0x", "")

    # Fix odd-length hex
    if len(hex_string) % 2 != 0:
        print("[!] Warning: hex length is odd. Padding with leading zero.")
        hex_string = "0" + hex_string

    # CGI must contain at least 7 bytes (14 hex chars)
    if len(hex_string) < 14:
        raise ValueError("Hex string must contain at least 14 hex digits (7 bytes).")

    # Use ONLY the first 7 bytes (standard CGI structure)
    b = bytes.fromhex(hex_string[:14])

    b0, b1, b2 = b[0], b[1], b[2]

    # Split nibbles
    b0_low  = b0 & 0x0F
    b0_high = (b0 >> 4) & 0x0F
    b1_low  = b1 & 0x0F
    b1_high = (b1 >> 4) & 0x0F
    b2_low  = b2 & 0x0F
    b2_high = (b2 >> 4) & 0x0F

    # ---------------------------
    # Decode MCC
    # ---------------------------
    MCC = f"{b0_low}{b0_high}{b1_low}"

    # ---------------------------
    # Decode MNC
    # Fully correct 3GPP logic
    # ---------------------------
    if b1_high == 0xF:
        # MNC length = 1 or 2 digits
        if b2_low == 0:
            MNC = f"{b2_high}"  # 1-digit MNC
        else:
            MNC = f"{b2_high}{b2_low}"  # 2-digit MNC
    else:
        # Full 3-digit MNC
        MNC = f"{b1_high}{b2_high}{b2_low}"

    # ---------------------------
    # Decode LAC + CI
    # ---------------------------
    LAC = b[3] * 256 + b[4]
    CI  = b[5] * 256 + b[6]

    return MCC, MNC, LAC, CI


def pretty_print(MCC, MNC, LAC, CI):
    print("\n────────────── Decoded CGI ──────────────")
    print(f"• MCC : {MCC}")
    print(f"• MNC : {MNC}")
    print(f"• LAC : {LAC}   (0x{LAC:04X})")
    print(f"• CI  : {CI}    (0x{CI:04X})")
    print("─────────────────────────────────────────\n")


# Entry point
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\nUsage: python cellid_decoder.py <hex_value>")
        print("Example:")
        print("  python cellid_decoder.py 02f80257ee0452\n")
        sys.exit(1)

    hex_value = sys.argv[1]
    MCC, MNC, LAC, CI = decode_cgid(hex_value)
    pretty_print(MCC, MNC, LAC, CI)
