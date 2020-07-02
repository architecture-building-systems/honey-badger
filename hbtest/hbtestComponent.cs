using System;
using System.Collections.Generic;
using System.Drawing;
using System.IO;
using System.Text;
using System.Windows.Forms;
using Grasshopper.Kernel;
using Microsoft.Scripting;
using Microsoft.Scripting.Hosting;
using Rhino;
using RhinoPython;
using IronPython;
using IronPython.Hosting;

// In order to load the result of this wizard, you will also need to
// add the output bin/ folder of this project to the list of loaded
// folder in Grasshopper.
// You can use the _GrasshopperDeveloperSettings Rhino command for that.

namespace hbtest
{
    public class hbtestComponent : GH_Component
    {
        /// <summary>
        /// Each implementation of GH_Component must provide a public 
        /// constructor without any arguments.
        /// Category represents the Tab in which the component will appear, 
        /// Subcategory the panel. If you use non-existing tab or panel names, 
        /// new tabs/panels will automatically be created.
        /// </summary>
        public hbtestComponent()
          : base("hbtest", "Nickname",
              "Description",
              "Category", "Subcategory")
        {
        }

        /// <summary>
        /// Registers all the input parameters for this component.
        /// </summary>
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
        }

        /// <summary>
        /// Registers all the output parameters for this component.
        /// </summary>
        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
        }

        /// <summary>
        /// This is the method that actually does the work.
        /// </summary>
        /// <param name="DA">The DA object can be used to retrieve data from input parameters and 
        /// to store data in output parameters.</param>
        protected override void SolveInstance(IGH_DataAccess DA)
        {
            var path = @"C:\Users\darthoma\Documents\GitHub\honey-badger\examples\helloworld\helloworld.py";
            var runtimeSetup = Python.CreateRuntimeSetup((IDictionary<string, object>)null);
            runtimeSetup.Options.Add("DivisionOptions", (object)PythonDivisionOptions.New);
            runtimeSetup.Options.Add("Frames", (object)true);
            runtimeSetup.Options.Add("Tracing", (object)true);
            ScriptRuntime scriptRuntime = new ScriptRuntime(runtimeSetup);
            scriptRuntime.LoadAssembly(typeof(RhinoApp).Assembly);
            scriptRuntime.LoadAssembly(typeof(int).Assembly);
            scriptRuntime.LoadAssembly(typeof(Form).Assembly);
            scriptRuntime.LoadAssembly(typeof(Color).Assembly);
            scriptRuntime.LoadAssembly(typeof(LengthExtension).Assembly);

            var engine = scriptRuntime.GetEngine("py");
            var stream = new hbtestStdioStream();

            scriptRuntime.IO.SetErrorOutput((Stream)stream, Encoding.Default);
            scriptRuntime.IO.SetOutput((Stream)stream, Encoding.Default);
            scriptRuntime.IO.SetInput((Stream)stream, Encoding.Default);
            
            ScriptScope scope = engine.CreateScope();
            ScriptSource scriptSourceFromFile = engine.CreateScriptSourceFromFile(
                path, Encoding.Default, SourceCodeKind.Statements);
            scriptSourceFromFile.Execute(scope);

            var main = scope.GetVariable("main");
            var result = main("hello, world");
            RhinoApp.WriteLine($"executed: {result}");
        }

        /// <summary>
        /// Provides an Icon for every component that will be visible in the User Interface.
        /// Icons need to be 24x24 pixels.
        /// </summary>
        protected override System.Drawing.Bitmap Icon
        {
            get
            {
                // You can add image files to your project resources and access them like this:
                //return Resources.IconForThisComponent;
                return null;
            }
        }

        /// <summary>
        /// Each component must have a unique Guid to identify it. 
        /// It is vital this Guid doesn't change otherwise old ghx files 
        /// that use the old ID will partially fail during loading.
        /// </summary>
        public override Guid ComponentGuid
        {
            get { return new Guid("d38910f6-af7c-4a29-aa0c-56515facf8c8"); }
        }
    }

    public class hbtestStdioStream : Stream
    {
        private readonly StringBuilder sb = new StringBuilder();

        public override bool CanRead => true;

        public override bool CanSeek => false;

        public override bool CanWrite => true;

        public override void Flush()
        {
        }

        public override long Length => throw new Exception("The method or operation is not implemented.");

        public override long Position
        {
            get
            {
                throw new Exception("The method or operation is not implemented.");
            }
            set
            {
                throw new Exception("The method or operation is not implemented.");
            }
        }


        public override long Seek(long offset, SeekOrigin origin) => throw new Exception("The method or operation is not implemented.");

        public override void SetLength(long value) => throw new Exception("The method or operation is not implemented.");
        public override int Read(byte[] buffer, int offset, int count)
        {
            throw new NotImplementedException();
        }

        public override void Write(byte[] buffer, int offset, int count)
        {
            string str = Encoding.Default.GetString(buffer, offset, count).Replace("\r", "");
            this.sb.Append(str);
            if (str.EndsWith("\n"))
            {
                RhinoApp.Write(this.sb.ToString());
                this.sb.Length = 0;
            }
        }
    }
}
