using Microsoft.AspNetCore.Mvc;

namespace MiApi.Controllers;

public record Product(int Id, string Name, decimal Price);

[ApiController]
[Route("api/[controller]")]
public class ProductsController : ControllerBase
{
    private static readonly List<Product> Products = new()
    {
        new Product(1, "Mecanical keyboard", 79.90m),
        new Product(2, "Wireless mouse", 39.50m)
    };

    [HttpGet]
    public IActionResult GetAll() => Ok(Products);

    [HttpGet("{id:int}")]
    public IActionResult GetById(int id)
    {
        var product = Products.FirstOrDefault(p => p.Id == id);

        return product is null
            ? NotFound()
            : Ok(product);
    }

    [HttpPost]
    public IActionResult Create(Product product)
    {
        Products.Add(product);
        return CreatedAtAction(nameof(GetById), new { id = product.Id }, product);
    }
}