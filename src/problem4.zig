const std = @import("std");
const zeit = @import("zeit");

fn parseLine(line: []const u8) struct { []const u8, []const u8 } {
    var i: u8 = 11;
    std.debug.print("{d}\n", .{line[i]});
    while (line[i] != ' ') {
        i += 1;
    }
    const tzEnd = i;
    while (line[i] == ' ') {
        i += 1;
    }

    return .{ line[11..tzEnd], line[i..] };
}

// There's probably some way to do this better
fn stringToTimeZone(str: []const u8) !zeit.Location {
    for (std.enums.values(zeit.Location)) |f| {
        if (std.mem.eql(u8, f.asText(), str)) {
            return f;
        }
    }

    std.debug.print("no match {s}\n", .{str});
    return error.Invalid;
}

pub fn answer(lines: std.mem.SplitIterator(u8, .scalar)) !void {
    const alloc = std.heap.page_allocator;
    var foo = lines;
    while (foo.next()) |source_line| {
        if (source_line.len == 0) {
            break;
        }

        const dest_line = foo.next().?;

        const parsed_source = parseLine(source_line);
        const parsed_dest = parseLine(dest_line);

        const source_location = try stringToTimeZone(parsed_source[0]);
        const dest_location = try stringToTimeZone(parsed_dest[0]);

        std.debug.print("{any}\n", .{source_location});

        const dest_timezone = zeit.loadTimeZone(alloc, source_location, null);
        const source_timezone = zeit.loadTimeZone(alloc, dest_location, null);

        std.debug.print("{any}\n", .{source_timezone});
        std.debug.print("{any}\n", .{dest_timezone});

        _ = foo.next();
    }
}

test "test this" {
    const testString = "Departure: Europe/London                  Mar 04, 2020, 10:00";
    const parsed = parseLine(testString);
    std.debug.print("{s}\n", .{parsed[0]});
    std.debug.print("{s}\n", .{parsed[1]});

    const zone = try zeit.loadTimeZone(std.heap.page_allocator);
    std.debug.print("{any}\n", .{zone});

    // if (std.mem.eql(u8, testString[0..12], "Departure: ")) {} else if (std.mem.eql(u8, testString[0..12], "Arrival:   ")) {
    //     var i = 12;
    // }
    // var iter = std.mem.split(u8, testString, ' ');
    // while (iter.next()) |part| {
    //     std.debug.print("{s}\n", .{part});
    // }
    try std.testing.expect(1 == 1);
}
