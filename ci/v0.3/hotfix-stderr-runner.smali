.class public final La/z;
.super Ljava/lang/Object;
.source "SourceFile"

# interfaces
.implements Ljava/lang/Runnable;

# instance fields
.field private final a:La/d;
.field private final b:Ljava/lang/Process;

# direct methods
.method public constructor <init>(La/d;Ljava/lang/Process;)V
    .locals 0

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V
    iput-object p1, p0, La/z;->a:La/d;
    iput-object p2, p0, La/z;->b:Ljava/lang/Process;
    return-void
.end method

# virtual methods
.method public final run()V
    .locals 4

    :try_start_0
    new-instance v0, Ljava/io/BufferedReader;
    new-instance v1, Ljava/io/InputStreamReader;
    iget-object v2, p0, La/z;->b:Ljava/lang/Process;
    invoke-virtual {v2}, Ljava/lang/Process;->getErrorStream()Ljava/io/InputStream;
    move-result-object v2
    sget-object v3, Ljava/nio/charset/StandardCharsets;->UTF_8:Ljava/nio/charset/Charset;
    invoke-direct {v1, v2, v3}, Ljava/io/InputStreamReader;-><init>(Ljava/io/InputStream;Ljava/nio/charset/Charset;)V
    invoke-direct {v0, v1}, Ljava/io/BufferedReader;-><init>(Ljava/io/Reader;)V

    :goto_0
    iget-object v1, p0, La/z;->a:La/d;
    iget-object v1, v1, La/d;->f:Ljava/util/concurrent/atomic/AtomicBoolean;
    invoke-virtual {v1}, Ljava/util/concurrent/atomic/AtomicBoolean;->get()Z
    move-result v1
    if-nez v1, :cond_1
    invoke-virtual {v0}, Ljava/io/BufferedReader;->readLine()Ljava/lang/String;
    move-result-object v1
    if-eqz v1, :cond_1
    iget-object v2, p0, La/z;->a:La/d;
    invoke-virtual {v2, v1}, La/d;->m(Ljava/lang/String;)V
    goto :goto_0

    :cond_1
    invoke-virtual {v0}, Ljava/io/BufferedReader;->close()V
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    :catch_0
    return-void
.end method
