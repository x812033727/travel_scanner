using System.Net.Http;
using System.Net.Http.Json;

// NoteVault (fixed): the signing secret is gone from the client.
// Activation is decided by the server; the client only sends the key
// and receives "approved" or not. Built as a reverse-engineering
// test target for a Mokaair video. No secret value is baked in here.
namespace NoteVault;

internal static class Program
{
    private static async Task<int> Main(string[] args)
    {
        if (args.Length >= 2 && args[0] == "activate")
        {
            var ok = await License.Verify(args[1]);
            Console.WriteLine(ok ? "Pro activated." : "Invalid license key.");
            return ok ? 0 : 1;
        }
        Console.WriteLine($"NoteVault {Sync.Version}. Commands: activate <key>");
        return 0;
    }
}

internal static class License
{
    // No secret here. Only the address of the server that holds it.
    private static readonly string VerifyUrl =
        Environment.GetEnvironmentVariable("NV_LICENSE_URL")
        ?? "http://127.0.0.1:8799/license/verify";

    public static async Task<bool> Verify(string key)
    {
        using var http = new HttpClient();
        var res = await http.PostAsJsonAsync(VerifyUrl, new { key });
        var body = await res.Content.ReadFromJsonAsync<Reply>();
        return body?.approved == true;
    }

    private sealed record Reply(bool approved);
}

internal static class Sync
{
    public const string Version = "2.0.0";
}
