const std = @import("std");
const problem1 = @import("problem1.zig");
const problem2 = @import("problem2.zig");
const problem3 = @import("problem3.zig");
const problem4 = @import("problem4.zig");
const problem5 = @import("problem5.zig");
const problem6 = @import("problem6.zig");

pub fn main() !void {
    var iter = std.process.args();
    _ = iter.next();
    const problem = iter.next().?;
    const input_file_name = iter.next().?;

    var input_file = try std.fs.cwd().openFile(input_file_name, .{});
    defer input_file.close();

    const lines = try input_file.readToEndAlloc(std.heap.page_allocator, 2_000_000);
    const splits = std.mem.splitScalar(u8, lines, '\n');

    if (std.mem.eql(u8, problem, "problem1")) {
        try problem1.answer(splits);
    } else if (std.mem.eql(u8, problem, "problem2")) {
        try problem2.answer(splits);
    } else if (std.mem.eql(u8, problem, "problem3")) {
        try problem3.answer(splits);
    } else if (std.mem.eql(u8, problem, "problem4")) {
        try problem4.answer(splits);
    } else if (std.mem.eql(u8, problem, "problem5")) {
        try problem5.answer(splits);
    } else if (std.mem.eql(u8, problem, "problem6")) {
        try problem6.answer(splits);
    } else {
        return error.InvalidProblem;
    }
}
