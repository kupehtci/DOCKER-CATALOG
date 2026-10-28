using Microsoft.OpenApi;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();

builder.Services.AddSwaggerGen(options =>
{
    options.SwaggerDoc("v1", new OpenApiInfo
    {
        Title = "MyApi",
        Version = "v1",
        Description = "API de ejemplo con .NET y Swagger"
    });
});

// Add healthcheck for the Docker compose health check.
builder.Services.AddHealthChecks();

var app = builder.Build();

app.MapHealthChecks("/health");

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI(options =>
    {
        options.SwaggerEndpoint("/swagger/v1/swagger.json", "Mi API v1");
        options.RoutePrefix = "swagger";
    });
}

// No HTTPS redirection: the container only listens on HTTP (TLS is terminated by a reverse proxy)
app.UseAuthorization();
app.MapControllers();

app.Run();