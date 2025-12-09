load("@rules_cc//cc:defs.bzl", "cc_binary")

cc_binary(
  name = "main",
  srcs = ["main.cc"],
  deps = [
    # Personal deps:
    "//console:console",
    # External deps:
    "@abseil-cpp//absl/strings",
  ],
)
