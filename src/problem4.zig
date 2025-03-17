const std = @import("std");
const zdt = @import("zdt");

fn parseLine(line: []const u8) struct { []const u8, []const u8 } {
    var i: u8 = 11;
    while (line[i] != ' ') {
        i += 1;
    }
    const tzEnd = i;
    while (line[i] == ' ') {
        i += 1;
    }

    return .{ line[11..tzEnd], line[i..] };
}

fn tzLocalizeFallback(dt: zdt.Datetime, opts: ?zdt.Datetime.tz_options) zdt.ZdtError!zdt.Datetime {
    return zdt.Datetime.fromFields(.{
        .year = dt.year,
        .month = dt.month,
        .day = dt.day,
        .hour = dt.hour,
        .minute = dt.minute,
        .second = dt.second,
        .nanosecond = dt.nanosecond,
        .tz_options = opts,
        .dst_fold = 1,
    });
}

pub fn answer(lines: std.mem.SplitIterator(u8, .scalar)) !void {
    const allocator = std.heap.page_allocator;
    var foo = lines;
    var total_seconds: i64 = 0;
    while (foo.next()) |source_line| {
        if (source_line.len == 0) {
            break;
        }

        const dest_line = foo.next().?;

        const parsed_source = parseLine(source_line);
        const parsed_dest = parseLine(dest_line);

        var source_tz = try zdt.Timezone.fromTzdata(parsed_source[0], allocator);
        var dest_tz = try zdt.Timezone.fromTzdata(parsed_dest[0], allocator);
        defer source_tz.deinit();
        defer dest_tz.deinit();

        // std.debug.print("{s}\n", .{source_tz.name()});
        // std.debug.print("{s}\n", .{dest_tz.name()});

        // std.debug.print("{s}\n", .{parsed_source[1]});
        // std.debug.print("{s}\n", .{parsed_dest[1]});

        const source_timestamp = try zdt.Datetime.fromString(parsed_source[1], "%b %d, %Y, %H:%M");
        const dest_timestamp = try zdt.Datetime.fromString(parsed_dest[1], "%b %d, %Y, %H:%M");

        const source_localized = source_timestamp.tzLocalize(.{ .tz = &source_tz }) catch try tzLocalizeFallback(source_timestamp, .{ .tz = &source_tz });
        const dest_localized = dest_timestamp.tzLocalize(.{ .tz = &dest_tz }) catch try tzLocalizeFallback(dest_timestamp, .{ .tz = &source_tz });

        const delta = @divTrunc((dest_localized.unix_sec - source_localized.unix_sec), 60);
        std.debug.print("{d}\n", .{delta});

        total_seconds += delta;
        _ = foo.next();
    }

    std.debug.print("{d}\n", .{total_seconds});
}
