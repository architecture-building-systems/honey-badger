using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Grasshopper.Kernel.Special;

namespace HoneyBadgerRuntime
{
    /// <summary>
    /// Abstract base class for all honey badger value lists.
    /// </summary>
    public abstract class HoneyBadgerValueList : GH_ValueList
    {
        private string m_guid;

        /// <summary>
        /// Subclasses are expected to implement a default contructor that calls this one with d
        /// </summary>
        /// <param name="name"></param>
        /// <param name="nickname"></param>
        /// <param name="description"></param>
        /// <param name="category"></param>
        /// <param name="subCategory"></param>
        public HoneyBadgerValueList(string name, string nickname, string description, string category, string subCategory, string guid) : base()
        {
            this.Name = name;
            this.NickName = nickname;
            this.Description = description;
            this.Category = category;
            this.SubCategory = subCategory;

            this.m_guid = guid;

            this.ListItems.Clear();
            this.ListItems.Add(new GH_ValueListItem("Testing", "did it work?"));
            this.ListItems.Add(new GH_ValueListItem("Testing2", "did it work?"));
        }

        public override Guid ComponentGuid
        {
            get
            {
                return new Guid(this.m_guid);
            }
        }
    }
}
