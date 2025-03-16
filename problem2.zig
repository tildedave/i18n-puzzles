const std = @import("std");
var allocator = std.heap.page_allocator;

const ctime = @cImport({
    @cInclude("time.h");
});
const testInput = @embedFile("input2-test.txt");
const input = @embedFile("input2.txt");

pub fn main() !void {
    var splits = std.mem.splitScalar(u8, input, '\n');
    var map = std.AutoHashMap(ctime.time_t, u8).init(allocator);
    defer map.deinit();

    var result: ctime.time_t = 0;
    while (splits.next()) |line| {
        if (line.len == 0) {
            continue;
        }

        var newLine = try removeColon(line);
        const dateFormat = "%Y-%m-%dT%H:%M:%S%z";
        var time: ctime.tm = std.mem.zeroes(ctime.tm);
        _ = ctime.strptime(&newLine[0], dateFormat, &time);

        const gmt: ctime.time_t = ctime.mktime(&time);
        const num = map.get(gmt) orelse 0;
        if (num == 3) {
            result = gmt;
            break;
        }
        try map.put(gmt, num + 1);
    }

    if (result == 0) {
        return error.NotFound;
    }

    var answer: [255]u8 = undefined;
    const backout = ctime.gmtime(&result);
    const bytesWritten = ctime.strftime(&answer, 255, "%Y-%m-%dT%H:%M:%S", backout);
    std.debug.print("{s}+00:00\n", .{answer[0..bytesWritten]});
}

pub fn removeColon(line: []const u8) ![]u8 {
    // The dates have offsets like +00:00
    // Unfortunately C's strptime doesn't want the colon, and it throws a
    // parsing error.
    // So we will remove it.

    var i: usize = line.len;
    var newLine = try allocator.alloc(u8, line.len - 1);
    while (i > 0) {
        i -= 1;
        if (line[i] == ':') {
            @memcpy(newLine[0..i], line[0..i]);
            @memcpy(newLine[i..], line[i + 1 ..]);
            break;
        }
    }
    if (i == 0) {
        return error.NotFound;
    }

    return newLine;
}
