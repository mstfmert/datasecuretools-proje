export async function onRequest(context) {
  const { searchParams } = new URL(context.request.url);
  const ip = searchParams.get('ip');

  if (!ip) return new Response('IP Required', { status: 400 });

  // İsteği sunucu tarafında Cloudflare üzerinden yapıyoruz (CORS bypass)
  const response = await fetch(`https://ipapi.co/${ip}/json/`);
  const data = await response.json();

  return new Response(JSON.stringify(data), {
    headers: { 
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*' 
    }
  });
}