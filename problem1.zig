const std = @import("std");
const unicode = @import("std.unicode");
const testInput = @embedFile("input1-test.txt");
const input = @embedFile("input1.txt");

pub fn main() !void {
    var splits = std.mem.splitScalar(u8, input, '\n');
    var charge: u64 = 0;

    while (splits.next()) |line| {
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

    // var file = try std.fs.cwd().openFile("input1-test.txt", .{});
    // defer file.close();

    // // const stdout = std.io.getStdOut().writer();
    // // try stdout.print("Hello, {s}!\n", .{"world"});
}
