const std = @import("std");
const ziglyph = @import("ziglyph");
const unicode = @import("std").unicode;

pub fn answer(lines: std.mem.SplitIterator(u8, .scalar)) !void {
    var foo = lines;
    var valid: u64 = 0;
    while (foo.next()) |line| {
        if (line.len == 0) {
            break;
        }
        const result = validatePassword(line);
        if (result) |_| {
            valid += 1;
        } else |_| {}
        std.debug.print("{s} {any}\n", .{ line, result });
    }
    std.debug.print("{d}\n", .{valid});
}

pub fn validatePassword(line: []const u8) !bool {
    // character length between 4 and at most 12
    // one digit (ASCII)
    // one uppercase letter (codepoint specific I imagine)
    // one lowercase letter (codepoint specific I imagine)
    // one character outside of ASCII
    const length = try std.unicode.utf8CountCodepoints(line);
    if (length < 4 or length > 12) {
        return error.InvalidLength;
    }

    var has_digit = false;
    var has_non_ascii = false;
    var has_upper = false;
    var has_lower = false;

    var code_point_iterator = (try unicode.Utf8View.init(line)).iterator();

    while (code_point_iterator.nextCodepoint()) |cp| {
        // std.debug.print("0x{x} is {u} isNonAscii {any} isUpper {any} isLower {any}\n", .{ cp, cp, cp > 0xFF, ziglyph.isUpper(cp), ziglyph.isLower(cp) });
        if (cp >= 0x30 and cp <= 0x39) {
            has_digit = true;
        }
        if (cp > 127) {
            has_non_ascii = true;
        }
        if (ziglyph.isUpper(cp)) {
            has_upper = true;
        }
        if (ziglyph.isLower(cp)) {
            has_lower = true;
        }
    }

    if (!has_digit) {
        return error.NoDigit;
    }

    if (!has_non_ascii) {
        return error.NoNonAscii;
    }

    if (!has_upper) {
        return error.NoUpper;
    }

    if (!has_lower) {
        return error.NoLower;
    }

    return true;
}
