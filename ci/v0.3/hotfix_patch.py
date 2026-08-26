from pathlib import Path
import sys

root = Path(sys.argv[1])
p = root / "smali/a/d.smali"
s = p.read_text()

# Preserve an in-memory tail of Codex stderr so Android UI errors expose the real native failure.
assert ".field public g:J\n" in s
s = s.replace(".field public g:J\n", ".field public g:J\n\n.field public final h:Ljava/lang/StringBuffer;\n", 1)

old = """    iput-object v0, p0, La/d;->f:Ljava/util/concurrent/atomic/AtomicBoolean;\n\n    const-wide/16 v0, 0x1\n"""
new = """    iput-object v0, p0, La/d;->f:Ljava/util/concurrent/atomic/AtomicBoolean;\n\n    new-instance v0, Ljava/lang/StringBuffer;\n\n    invoke-direct {v0}, Ljava/lang/StringBuffer;-><init>()V\n\n    iput-object v0, p0, La/d;->h:Ljava/lang/StringBuffer;\n\n    const-wide/16 v0, 0x1\n"""
assert old in s
s = s.replace(old, new, 1)

# Match the pinned Codex CLI spelling and version shown in initialize client metadata.
assert 'const-string v6, "appServer"' in s
s = s.replace('const-string v6, "appServer"', 'const-string v6, "app-server"', 1)
assert 'const-string v5, "0.3.0"' in s
s = s.replace('const-string v5, "0.3.0"', 'const-string v5, "0.3.1"', 1)

# Enable native backtraces, reset stderr tail before launch.
old = """    invoke-interface {v0, v2, v3}, Ljava/util/Map;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;\n\n    invoke-virtual {v1}, Ljava/lang/ProcessBuilder;->start()Ljava/lang/Process;\n"""
new = """    invoke-interface {v0, v2, v3}, Ljava/util/Map;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;\n\n    invoke-virtual {v1}, Ljava/lang/ProcessBuilder;->environment()Ljava/util/Map;\n\n    move-result-object v0\n\n    const-string v2, "RUST_BACKTRACE"\n\n    const-string v3, "1"\n\n    invoke-interface {v0, v2, v3}, Ljava/util/Map;->put(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;\n\n    iget-object v0, p0, La/d;->h:Ljava/lang/StringBuffer;\n\n    const/4 v2, 0x0\n\n    invoke-virtual {v0, v2}, Ljava/lang/StringBuffer;->setLength(I)V\n\n    invoke-virtual {v1}, Ljava/lang/ProcessBuilder;->start()Ljava/lang/Process;\n"""
assert old in s
s = s.replace(old, new, 1)

# Swap the old drain-that-discards-lines lambda for our tail-preserving Runnable.
old = """    new-instance v1, Ljava/lang/Thread;\n\n    new-instance v3, La/a;\n\n    const/4 v4, 0x0\n\n    invoke-direct {v3, p0, v0, v4}, La/a;-><init>(Ljava/lang/Object;Ljava/lang/Object;I)V\n\n    const-string v0, "Jarvis-codex-stderr"\n"""
new = """    new-instance v1, Ljava/lang/Thread;\n\n    new-instance v3, La/z;\n\n    invoke-direct {v3, p0, v0}, La/z;-><init>(La/d;Ljava/lang/Process;)V\n\n    const-string v0, "Jarvis-codex-stderr"\n"""
assert old in s
s = s.replace(old, new, 1)

# Pinned Codex intentionally omits the JSON-RPC version field on the wire.
for old in [
    """    const-string v2, "jsonrpc"\n\n    const-string v3, "2.0"\n\n    invoke-virtual {v1, v2, v3}, Lorg/json/JSONObject;->put(Ljava/lang/String;Ljava/lang/Object;)Lorg/json/JSONObject;\n\n    move-result-object v1\n\n""",
    """    const-string v2, "jsonrpc"\n\n    const-string v3, "2.0"\n\n    invoke-virtual {v1, v2, v3}, Lorg/json/JSONObject;->put(Ljava/lang/String;Ljava/lang/Object;)Lorg/json/JSONObject;\n\n    move-result-object v1\n\n""",
    """    const-string v3, "jsonrpc"\n\n    const-string v4, "2.0"\n\n    invoke-virtual {v2, v3, v4}, Lorg/json/JSONObject;->put(Ljava/lang/String;Ljava/lang/Object;)Lorg/json/JSONObject;\n\n    move-result-object v2\n\n""",
]:
    assert old in s
    s = s.replace(old, "", 1)

# Replace readMessage: never call exitValue while the process is alive, and append native stderr.
start = s.index(".method public final e()Lorg/json/JSONObject;")
end = s.index(".end method", start) + len(".end method")
new_e = r'''.method public final e()Lorg/json/JSONObject;
    .locals 5

    iget-object v0, p0, La/d;->d:Ljava/io/BufferedReader;
    if-eqz v0, :cond_5

    :catch_0
    :goto_0
    iget-object v0, p0, La/d;->d:Ljava/io/BufferedReader;
    invoke-virtual {v0}, Ljava/io/BufferedReader;->readLine()Ljava/lang/String;
    move-result-object v0
    if-eqz v0, :cond_1
    invoke-virtual {v0}, Ljava/lang/String;->trim()Ljava/lang/String;
    move-result-object v0
    invoke-virtual {v0}, Ljava/lang/String;->isEmpty()Z
    move-result v1
    if-eqz v1, :cond_0
    goto :goto_0

    :cond_0
    :try_start_0
    new-instance v1, Lorg/json/JSONObject;
    invoke-direct {v1, v0}, Lorg/json/JSONObject;-><init>(Ljava/lang/String;)V
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0
    return-object v1

    :cond_1
    iget-object v0, p0, La/d;->b:Ljava/lang/Process;
    if-nez v0, :cond_2
    new-instance v0, Ljava/lang/IllegalStateException;
    new-instance v1, Ljava/lang/StringBuilder;
    const-string v2, "Codex app-server closed stdout"
    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V
    invoke-virtual {p0}, La/d;->n()Ljava/lang/String;
    move-result-object v2
    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;
    move-result-object v1
    invoke-direct {v0, v1}, Ljava/lang/IllegalStateException;-><init>(Ljava/lang/String;)V
    throw v0

    :cond_2
    invoke-virtual {v0}, Ljava/lang/Process;->isAlive()Z
    move-result v1
    if-eqz v1, :cond_3
    new-instance v0, Ljava/lang/IllegalStateException;
    new-instance v1, Ljava/lang/StringBuilder;
    const-string v2, "Codex app-server closed stdout while still running"
    invoke-direct {v1, v2}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V
    invoke-virtual {p0}, La/d;->n()Ljava/lang/String;
    move-result-object v2
    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;
    move-result-object v1
    invoke-direct {v0, v1}, Ljava/lang/IllegalStateException;-><init>(Ljava/lang/String;)V
    throw v0

    :cond_3
    invoke-virtual {v0}, Ljava/lang/Process;->exitValue()I
    move-result v0
    new-instance v1, Ljava/lang/IllegalStateException;
    new-instance v2, Ljava/lang/StringBuilder;
    const-string v3, "Codex app-server exited ("
    invoke-direct {v2, v3}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V
    invoke-virtual {v2, v0}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;
    const-string v0, ")"
    invoke-virtual {v2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    invoke-virtual {p0}, La/d;->n()Ljava/lang/String;
    move-result-object v0
    invoke-virtual {v2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;
    move-result-object v0
    invoke-direct {v1, v0}, Ljava/lang/IllegalStateException;-><init>(Ljava/lang/String;)V
    throw v1

    :cond_5
    new-instance v0, Ljava/lang/IllegalStateException;
    const-string v1, "Codex stdout is unavailable"
    invoke-direct {v0, v1}, Ljava/lang/IllegalStateException;-><init>(Ljava/lang/String;)V
    throw v0
.end method'''
s = s[:start] + new_e + s[end:]

# Helpers for bounded stderr tail and suffix rendering.
insert_at = s.index(".method public final k(Lorg/json/JSONObject;)V")
helpers = r'''.method public final m(Ljava/lang/String;)V
    .locals 3
    iget-object v0, p0, La/d;->h:Ljava/lang/StringBuffer;
    invoke-virtual {v0}, Ljava/lang/StringBuffer;->length()I
    move-result v1
    if-lez v1, :cond_0
    const-string v1, "\n"
    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;
    :cond_0
    invoke-virtual {v0, p1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;
    invoke-virtual {v0}, Ljava/lang/StringBuffer;->length()I
    move-result p1
    const/16 v1, 0x2000
    if-le p1, v1, :cond_1
    sub-int/2addr p1, v1
    const/4 v2, 0x0
    invoke-virtual {v0, v2, p1}, Ljava/lang/StringBuffer;->delete(II)Ljava/lang/StringBuffer;
    :cond_1
    return-void
.end method

.method public final n()Ljava/lang/String;
    .locals 2
    iget-object v0, p0, La/d;->h:Ljava/lang/StringBuffer;
    invoke-virtual {v0}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;
    move-result-object v0
    invoke-virtual {v0}, Ljava/lang/String;->trim()Ljava/lang/String;
    move-result-object v0
    invoke-virtual {v0}, Ljava/lang/String;->isEmpty()Z
    move-result v1
    if-eqz v1, :cond_0
    const-string v0, ""
    return-object v0
    :cond_0
    new-instance v1, Ljava/lang/StringBuilder;
    const-string p0, "\n"
    invoke-direct {v1, p0}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V
    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;
    move-result-object v0
    return-object v0
.end method

'''
s = s[:insert_at] + helpers + s[insert_at:]

assert '"jsonrpc"' not in s
assert '"appServer"' not in s
assert '"app-server"' in s
assert '"0.3.1"' in s
assert 'La/d;->n()Ljava/lang/String;' in s
p.write_text(s)

# New stderr Runnable class, assembled alongside the existing optimized release classes.
(root / "smali/a/z.smali").write_text((Path(__file__).parent / "hotfix-stderr-runner.smali").read_text())
print("Patched", p)
