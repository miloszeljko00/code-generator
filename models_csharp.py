model_template = """
using System;

namespace HospitalLibrary.Core.Model
{
    public class {{ class.name }}
    {
    
        {% for property in class.properties -%}
        public {{ property.type }} {{ property.name }} { get; set; }
        
        {% endfor %}
    }
}
"""

repository_interface_template ="""
using HospitalLibrary.Core.Model;
using System.Collections.Generic;

namespace HospitalLibrary.Core.Repository
{
    public interface I{{class.name}}Repository
    {
        IEnumerable<{{class.name}}> GetAll();
        {{class.name}} GetBy{{class.properties[0].name}}({{class.properties[0].type}} {{class.properties[0].name.lower()}});
        void Create({{class.name}} {{class.name.lower()}});
        void Update({{class.name}} {{class.name.lower()}});
        void Delete({{class.name}} {{class.name.lower()}});
    }
}
"""

repository_template ="""
using HospitalLibrary.Core.Model;
using HospitalLibrary.Settings;
using Microsoft.EntityFrameworkCore;
using System.Collections.Generic;
using System.Linq;

namespace HospitalLibrary.Core.Repository
{
    public class {{class.name}}Repository : I{{class.name}}Repository
    {
        private readonly HospitalDbContext _context;

        public {{class.name}}Repository(HospitalDbContext context)
        {
            _context = context;
        }

        public IEnumerable<{{class.name}}> GetAll()
        {
            return _context.{{class.name}}s.ToList();
        }

        public {{class.name}} GetBy{{class.properties[0].name}}({{class.properties[0].type}} {{class.properties[0].name.lower()}})
        {
            return _context.{{class.name}}s.Find({{class.properties[0].name.lower()}});
        }

        public void Create({{class.name}} {{class.name.lower()}})
        {
            _context.{{class.name}}s.Add({{class.name.lower()}});
            _context.SaveChanges();
        }

        public void Update({{class.name}} {{class.name.lower()}})
        {
            _context.Entry({{class.name.lower()}}).State = EntityState.Modified;

            try
            {
                _context.SaveChanges();
            }
            catch (DbUpdateConcurrencyException)
            {
                throw;
            }
        }

        public void Delete({{class.name}} {{class.name.lower()}})
        {
            _context.{{class.name}}s.Remove({{class.name.lower()}});
            _context.SaveChanges();
        }
    }
}
"""

service_interface_template = """
using HospitalLibrary.Core.Model;
using System.Collections.Generic;

namespace HospitalLibrary.Core.Service
{
    public interface I{{class.name}}Service
    {
        IEnumerable<{{class.name}}> GetAll();
        {{class.name}} GetBy{{class.properties[0].name}}({{class.properties[0].type}} {{class.properties[0].name.lower()}});
        void Create({{class.name}} {{class.name.lower()}});
        void Update({{class.name}} {{class.name.lower()}});
        void Delete({{class.name}} {{class.name.lower()}});
    }
}
"""

service_template = """
using HospitalLibrary.Core.Model;
using HospitalLibrary.Core.Repository;
using System.Collections.Generic;

namespace HospitalLibrary.Core.Service
{
    public class {{class.name}}Service : I{{class.name}}Service
    {
        private readonly I{{class.name}}Repository _{{class.name.lower()}}Repository;

        public {{class.name}}Service(I{{class.name}}Repository {{class.name.lower()}}Repository)
        {
            _{{class.name.lower()}}Repository = {{class.name.lower()}}Repository;
        }

        public IEnumerable<{{class.name}}> GetAll()
        {
            return _{{class.name.lower()}}Repository.GetAll();
        }

        public {{class.name}} GetBy{{class.properties[0].name}}({{class.properties[0].type}} {{class.properties[0].name.lower()}})
        {
            return _{{class.name.lower()}}Repository.GetBy{{class.properties[0].name}}({{class.properties[0].name.lower()}});
        }

        public void Create({{class.name}} {{class.name.lower()}})
        {
            _{{class.name.lower()}}Repository.Create({{class.name.lower()}});
        }

        public void Update({{class.name}} {{class.name.lower()}})
        {
            _{{class.name.lower()}}Repository.Update({{class.name.lower()}});
        }

        public void Delete({{class.name}} {{class.name.lower()}})
        {
            _{{class.name.lower()}}Repository.Delete({{class.name.lower()}});
        }
    }
}
"""

controller_template = """
using HospitalLibrary.Core.Model;
using HospitalLibrary.Core.Service;
using Microsoft.AspNetCore.Mvc;

namespace HospitalAPI.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class {{class.name}}sController : ControllerBase
    {
        private readonly I{{class.name}}Service _{{class.name.lower()}}Service;

        public {{class.name}}sController(I{{class.name}}Service {{class.name.lower()}}Service)
        {
            _{{class.name.lower()}}Service = {{class.name.lower()}}Service;
        }

        [HttpGet]
        public ActionResult GetAll()
        {
            return Ok(_{{class.name.lower()}}Service.GetAll());
        }

        [HttpGet("{% raw %}{{% endraw %}{{class.properties[0].name.lower()}}{% raw %}}{% endraw %}")]
        public ActionResult GetBy{{class.properties[0].name}}({{class.properties[0].type}} {{class.properties[0].name.lower()}})
        {
            var {{class.name.lower()}} = _{{class.name.lower()}}Service.GetBy{{class.properties[0].name}}({{class.properties[0].name.lower()}});
            if ({{class.name.lower()}} == null)
            {
                return NotFound();
            }

            return Ok({{class.name.lower()}});
        }

        [HttpPost]
        public ActionResult Create({{class.name}} {{class.name.lower()}})
        {
            if (!ModelState.IsValid)
            {
                return BadRequest(ModelState);
            }

            _{{class.name.lower()}}Service.Create({{class.name.lower()}});
            return CreatedAtAction("GetBy{{class.properties[0].name}}", new { {{class.properties[0].name.lower()}} = {{class.name.lower()}}.{{class.properties[0].name}} }, {{class.name.lower()}});
        }

        [HttpPut("{% raw %}{{% endraw %}{{class.properties[0].name.lower()}}{% raw %}}{% endraw %}")]
        public ActionResult Update({{class.properties[0].type}} {{class.properties[0].name.lower()}}, {{class.name}} {{class.name.lower()}})
        {
            if (!ModelState.IsValid)
            {
                return BadRequest(ModelState);
            }

            if ({{class.properties[0].name.lower()}} != {{class.name.lower()}}.{{class.properties[0].name}})
            {
                return BadRequest();
            }

            try
            {
                _{{class.name.lower()}}Service.Update({{class.name.lower()}});
            }
            catch
            {
                return BadRequest();
            }

            return Ok({{class.name.lower()}});
        }

        [HttpDelete("{% raw %}{{% endraw %}{{class.properties[0].name.lower()}}{% raw %}}{% endraw %}")]
        public ActionResult Delete({{class.properties[0].type}} {{class.properties[0].name.lower()}})
        {
            var {{class.name.lower()}} = _{{class.name.lower()}}Service.GetBy{{class.properties[0].name}}({{class.properties[0].name.lower()}});
            if ({{class.name.lower()}} == null)
            {
                return NotFound();
            }

            _{{class.name.lower()}}Service.Delete({{class.name.lower()}});
            return NoContent();
        }
    }
}
"""