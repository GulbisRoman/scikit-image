using System;
using System.Collections.Generic;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices;
using System.Runtime.Serialization.Formatters.Binary;
using System.Text;
using System.Threading.Tasks;

namespace effective_live_game
{
    class Program
    {
        static int next(int value, int max)
        {
            value = value >= max ? value - max : value;
            value = value < 0 ? value + max : value;

            return value;
        }

        static long getMemory(object o)
        {
            long size = 0;
            using (Stream stream = new MemoryStream())
            {
                BinaryFormatter formatter = new BinaryFormatter();
                formatter.Serialize(stream, o);
                size = stream.Length;
            }

            return size;
        }

        static byte[,] evolve(byte[,] data)
        {
            int w = data.GetLength(0), h = data.GetLength(1);
            byte[,] field = (byte[,]) data.Clone();
            
            byte friendly_neighborhood = 0;
            for (int i = 0; i < w; i++)
                for (int j = 0; j < h; j++)
                {
                    friendly_neighborhood = (byte)(data[next(i - 1, w), next(j - 1, h)] + data[i, next(j - 1, h)] + data[next(i + 1, w), next(j - 1, h)] + data[next(i - 1, w), j] + data[next(i + 1, w), j] + data[next(i - 1, w), next(j + 1, h)] + data[i, next(j + 1, h)] + data[next(i + 1, w), next(j + 1, h)]);

                    if(data[i, j] == 1)
                        field[i, j] = (byte) ((friendly_neighborhood == 2 || friendly_neighborhood == 3) ? 1 : 0);
                    else
                        field[i, j] = (byte)((friendly_neighborhood == 3) ? 1 : 0);

                }

            return field;
        }

        static byte[] Load(string filename)
        {
            Bitmap bitmap = new Bitmap(filename);

            Rectangle rect = new Rectangle(0, 0, bitmap.Width, bitmap.Height);
            System.Drawing.Imaging.BitmapData bmpData =
                bitmap.LockBits(rect, System.Drawing.Imaging.ImageLockMode.ReadWrite,
                bitmap.PixelFormat);

            IntPtr ptr = bmpData.Scan0;

            int bytes = Math.Abs(bmpData.Stride) * bitmap.Height;
            byte[] rgbValues = new byte[bytes];

            System.Runtime.InteropServices.Marshal.Copy(ptr, rgbValues, 0, bytes);
            bitmap.UnlockBits(bmpData);

            return rgbValues;
        }

        static void Save(byte[] values, string filename)
        {
            Bitmap bitmap = new Bitmap("base.png");

            Rectangle rect = new Rectangle(0, 0, bitmap.Width, bitmap.Height);
            System.Drawing.Imaging.BitmapData bmpData =
                bitmap.LockBits(rect, System.Drawing.Imaging.ImageLockMode.ReadWrite,
                bitmap.PixelFormat);

            IntPtr ptr = bmpData.Scan0;

            System.Runtime.InteropServices.Marshal.Copy(values, 0, ptr, values.Length);
            bitmap.UnlockBits(bmpData);
            bitmap.Save(filename);
        }

        [DllImport("Kernel32.dll", SetLastError = true)]
        public static extern bool QueryPerformanceCounter(out long i);

        [DllImport("Kernel32.dll", SetLastError = true)]
        public static extern bool QueryPerformanceFrequency(out long i);

        static void Main(string[] args)
        {
            long time, newtime, freq;
            QueryPerformanceCounter(out time);
            
            byte[] base_values = Load("base.png");
            byte[,] field = new byte[100, 100];
            int i = 0, j = 0;

            for (int counter = 0; counter < base_values.Length; counter += (int)(base_values.Length / 10000))
            {
                field[i, j] = (byte)(base_values[counter] == 255 ? 1 : 0);
                i++;
                if (i == 100)
                {
                    i = 0;
                    j++;
                }
            }

            List<byte[,]> states = new List<byte[,]>();
            states.Add(field);

            for(int q = 0; q < 100; q++)
                states.Add(evolve(states[states.Count - 1]));

            Console.WriteLine("Memory: " + getMemory(states).ToString());

            //Save(s, "kek/" + 171.ToString("0000") + ".png");


            
            int u = 0;
            byte[] values;
            foreach (byte[,] s in states)
            {
                values = (byte[])(base_values.Clone());
                i = 0;
                j = 0;
                for (int counter = 0; counter < values.Length; counter += (values.Length / 10000))
                {
                    if (s[i, j] == 1)
                    {
                        values[counter] = 255;
                        values[counter + 1] = 255;
                        values[counter + 2] = 255;
                    }
                    else
                    {
                        values[counter] = 0;
                        values[counter + 1] = 0;
                        values[counter + 2] = 0;
                    }

                    i++;
                    if (i == 100)
                    {
                        i = 0;
                        j++;
                    }
                }

                u++;
                Save(values, "kek/" + u.ToString("0000") + ".png");
            }

            QueryPerformanceCounter(out newtime);
            QueryPerformanceFrequency(out freq);
            Console.WriteLine(((newtime - time) * 1000 / freq).ToString());
            Console.Read();
        }
    }
}
