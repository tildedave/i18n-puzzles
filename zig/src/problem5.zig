const std = @import("std");
const unicode = std.unicode;

pub fn answer(lines: std.mem.SplitIterator(u8, .scalar)) !void {
    const allocator = std.heap.page_allocator;
    var list = std.ArrayList(u21).init(allocator);
    var foo = lines;
    var width: u32 = 0;
    var height: u32 = 0;
    var foo2 = lines;

    while (foo2.next()) |line| {
        var my_width: u32 = 1;
        var cp_iter = (try unicode.Utf8View.init(line)).iterator();
        while (cp_iter.nextCodepoint()) |cp| {
            const loc = try list.addOne();
            loc.* = cp;
            my_width += 1;
        }
        if (my_width > width) {
            width = my_width;
        }
        height += 1;
    }

    std.debug.print("height = {d} width = {d}\n", .{ height, width });

    while (foo.next()) |line| {
        if (line.len == 0) {
            break;
        }
        var cp_iter = (try unicode.Utf8View.init(line)).iterator();
        var row_width: u32 = 1;
        while (cp_iter.nextCodepoint()) |cp| {
            const loc = try list.addOne();
            loc.* = cp;
            row_width += 1;
        }
        while (row_width < width) {
            const loc = try list.addOne();
            loc.* = ' ';
            row_width += 1;
        }
    }
    std.debug.print("{any} {d}\n", .{ list, list.items.len });

    var x: u32 = 0;
    var y: u32 = 0;
    while (y < height) {
        std.debug.print("{d},{d} {u}\n", .{ x, y, list.items[y * (width - 1) + x] });
        x = @mod(x + 2, width);
        y += 1;
    }
}
