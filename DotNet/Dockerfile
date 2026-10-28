ARG DOTNET_VERSION=10.0

FROM mcr.microsoft.com/dotnet/sdk:${DOTNET_VERSION} AS build
WORKDIR /src

# Adapt the *.sln or *.slnx to your application
COPY MyApi/MyApi.slnx ./
COPY MyApi/MyApi.csproj ./

# Restore dependencies (cached layer while the project files do not change)
RUN dotnet restore MyApi.slnx

# Copy the rest (bin/ and obj/ are excluded by .dockerignore)
COPY MyApi/ ./

# Compile and publish the Solution
RUN dotnet publish MyApi.slnx -c Release --no-restore -o /app/publish /p:UseAppHost=false

# The final layer that only contains the aspnet runtime and not the entire SDK
FROM mcr.microsoft.com/dotnet/aspnet:${DOTNET_VERSION} AS final
WORKDIR /app

# Install curl for the healthcheck (not included in the aspnet base image)
# and create a log directory owned by the non-root user
# APP_UID is defined in the .Net base image
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /app/logs \
    && chown -R $APP_UID:$APP_UID /app

# Run the app as a non-root user
USER $APP_UID

# Copy the compiled application
COPY --from=build --chown=$APP_UID:$APP_UID /app/publish .

# Adjust environmental variables for the application
ENV ASPNETCORE_URLS=http://+:8080 \
    DOTNET_EnableDiagnostics=0

EXPOSE 8080

# Adjust to your DLL name
ENTRYPOINT ["dotnet", "MyApi.dll"]
