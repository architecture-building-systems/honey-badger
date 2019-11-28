using System;
using System.Drawing;
using Grasshopper.Kernel;

namespace HoneyBadgerRuntime
{
    public class HoneyBadgerRuntimeInfo : GH_AssemblyInfo
  {
    public override string Name
    {
        get
        {
            return "HoneyBadgerRuntime";
        }
    }
    public override Bitmap Icon
    {
        get
        {
            //Return a 24x24 pixel bitmap to represent this GHA library.
            return null;
        }
    }
    public override string Description
    {
        get
        {
            //Return a short string describing the purpose of this GHA library.
            return "";
        }
    }
    public override Guid Id
    {
        get
        {
            return new Guid("648e75a6-1da4-432f-b620-e5756aa0445a");
        }
    }

    public override string AuthorName
    {
        get
        {
            //Return a string identifying you or your company.
            return "";
        }
    }
    public override string AuthorContact
    {
        get
        {
            //Return a string representing your preferred contact details.
            return "";
        }
    }
}
}
