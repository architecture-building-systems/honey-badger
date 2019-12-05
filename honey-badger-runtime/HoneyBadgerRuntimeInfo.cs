using System;
using System.Drawing;
using Grasshopper.Kernel;

namespace HoneyBadgerRuntime
{
    public abstract class HoneyBadgerRuntimeInfo : GH_AssemblyInfo
    {
        private readonly string m_name;
        private readonly string m_description;
        private readonly string m_id;

        /// <summary>
        /// Implements a GH_AssemblyInfo that can be used as a base class for Reflection.Emit in the honey-badger parameter compiler, which needs to provide the default constructor that calls this one.
        /// </summary>
        /// <param name="name"></param>
        /// <param name="description"></param>
        /// <param name="id"></param>
        public HoneyBadgerRuntimeInfo(string name, string description, string id)
        {
            this.m_name = name;
            this.m_description = description;
            this.m_id = id;
        }

        public override string Name
        {
            get
            {
                return this.m_name;
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
                return this.m_description;
            }
        }
        public override Guid Id
        {
            get
            {
                return new Guid(this.m_id);
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
