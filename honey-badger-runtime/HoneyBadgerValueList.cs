using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Grasshopper.Kernel.Expressions;
using Grasshopper.Kernel.Special;
using Grasshopper.Kernel.Data;

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
            this.LoadValueList();
        }

        /// <summary>
        /// Load the value list. NOTE: This is supposed to be overridden by the
        /// honey-badger parameter compiler.
        /// </summary>
        public virtual void LoadValueList()
        {
            this.AddListItem("first key", "first value");
            this.AddListItem("second key", "second value");
            this.AddListItem("third key", "third value");
        }

        /// <summary>
        /// Return the icon string (base64) from the icon provided in honey-badger. NOTE: This is
        /// supposed to be overridden by the honey-badger parameter compiler.
        /// </summary>
        /// <returns></returns>
        public virtual string GetIconString()
        {
            return null;
        }

        protected override Bitmap Icon
        {
            get
            {
                var iconBase64 = GetIconString();
                if (iconBase64 == null)
                {
                    return base.Icon;
                }

                return new Bitmap(
                    new System.IO.MemoryStream(System.Convert.FromBase64String(iconBase64)));
            }
        }


        public void AddListItem(string key, string value)
        {
            this.ListItems.Add(new GH_ValueListItem(key, value));
        }

        public override Guid ComponentGuid
        {
            get
            {
                return new Guid(this.m_guid);
            }
        }

        protected override void CollectVolatileData_Custom()
        {
            this.m_data.Clear();
            foreach (GH_ValueListItem item in this.SelectedItems)
            {
                GH_Variant value = new GH_Variant(item.Expression);
                this.m_data.Append(value.ToGoo(), new GH_Path(0));
            }
        }
    }
}
