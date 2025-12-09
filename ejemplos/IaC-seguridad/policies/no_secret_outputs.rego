package local.plan

deny[msg] {
  some k
  v := input.outputs[k]
  re_match("(?i)(key|secret|token|password)", sprintf("%v", [v]))
  msg := sprintf("Output '%s' revela posible secreto", [k])
}
