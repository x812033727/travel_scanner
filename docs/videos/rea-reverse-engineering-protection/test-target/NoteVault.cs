using System.Security.Cryptography;
using System.Text;

// NoteVault: a tiny note app with a paid "Pro" tier.
// Built only as a reverse-engineering test target for a Mokaair video.
// Every secret below is a made-up test value.
namespace NoteVault;

internal static class Program
{
    private static int Main(string[] args)
    {
        if (args.Length >= 2 && args[0] == "activate")
        {
            var ok = License.Check(args[1]);
            Console.WriteLine(ok ? "Pro activated." : "Invalid license key.");
            return ok ? 0 : 1;
        }
        if (args.Length >= 1 && args[0] == "export-pdf")
        {
            if (!License.IsPro()) { Console.WriteLine("PDF export is a Pro feature."); return 2; }
            Console.WriteLine("Exporting notes to PDF...");
            return 0;
        }
        if (Environment.GetEnvironmentVariable("NV_INTERNAL_DEBUG") == "letmein")
        {
            Console.WriteLine("internal debug menu: all Pro features unlocked");
            return 0;
        }
        Console.WriteLine($"NoteVault {Sync.Version}. Commands: activate <key>, export-pdf");
        Console.WriteLine($"Pro costs {Pricing.MonthlyPrice(Pricing.Region())} per month.");
        return 0;
    }
}

internal static class License
{
    // Shared secret baked into the client: the mistake this test is about.
    private const string SigningSecret = "nv-test-secret-7f3a9c";

    // Key format: NV-<6 digit user id>-<first 8 hex chars of HMAC-SHA256(secret, user id)>
    public static bool Check(string key)
    {
        var parts = key.Split('-');
        if (parts.Length != 3 || parts[0] != "NV" || parts[1].Length != 6) return false;
        using var hmac = new HMACSHA256(Encoding.UTF8.GetBytes(SigningSecret));
        var mac = Convert.ToHexString(hmac.ComputeHash(Encoding.UTF8.GetBytes(parts[1])))[..8];
        if (!string.Equals(mac, parts[2], StringComparison.OrdinalIgnoreCase)) return false;
        File.WriteAllText(LicensePath(), key);
        return true;
    }

    public static bool IsPro() => File.Exists(LicensePath()) && Check(File.ReadAllText(LicensePath()).Trim());

    private static string LicensePath() =>
        Path.Combine(Path.GetTempPath(), "notevault.license");
}

internal static class Pricing
{
    public static string Region() =>
        Environment.GetEnvironmentVariable("NV_REGION") ?? "TW";

    // Regional prices and a hidden 40% discount for region "EDU".
    public static string MonthlyPrice(string region) => region switch
    {
        "TW" => "NT$150",
        "JP" => "JPY 600",
        "EDU" => "NT$90",
        _ => "USD 4.99",
    };
}

internal static class Sync
{
    public const string Version = "1.4.2";
    public const string Endpoint = "https://sync.notevault.invalid/v2/notes";
    public const string ApiKey = "nvk_test_51HxQ2fakeKEY000000";
}
