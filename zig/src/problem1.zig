const std = @import("std");
const unicode = @import("std.unicode");

pub fn answer(lines: std.mem.SplitIterator(u8, .scalar)) !void {
    var foo = lines;
    var charge: u64 = 0;

    while (foo.next()) |line| {
        if (line.len == 0) {
            continue;
        }
        const smsValid = line.len <= 160;
        const numCodepoints = try std.unicode.utf8CountCodepoints(line);
        const tweetValid = numCodepoints <= 140;

        var cost: u8 = 0;
        if (smsValid and tweetValid) {
            cost = 13;
        } else if (smsValid) {
            cost = 11;
        } else if (tweetValid) {
            cost = 7;
        } else {
            cost = 0;
        }
        charge += cost;
    }

    std.debug.print("{d}\n", .{charge});
}
