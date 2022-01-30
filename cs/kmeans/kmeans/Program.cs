using System;
using System.Threading.Tasks;

namespace kmeans
{
    class Program
    {
        public struct Point
        {
            public Point(double x, double y, int clusterIndex = -1)
            {
                X = x;
                Y = y;
                ClusterIndex = clusterIndex;
            }

            public double X { get; set; }
            public double Y { get; set; }

            public int ClusterIndex { get; set; }


            public double Distance(Point A)
            {
                return Math.Sqrt(((A.X - X) * (A.X - X)) + ((A.Y - Y) * (A.Y - Y)));
            }
            public override string ToString() => $"{X.ToString().Replace(',','.')};{Y.ToString().Replace(',', '.')};{ClusterIndex}";
        }
        static Point[] ReadFile(string filename)
        {
            string text = System.IO.File.ReadAllText(filename);
            string[] byLine = text.Split('\n');
            Point[] result = new Point[byLine.Length - 2];
            int j = 0;
            for(int i = 0; i < byLine.Length; i++)
            {
                if (i == 0 || i == byLine.Length - 1) continue;
                string[] pair = byLine[i].Split(';');
                double x = Convert.ToDouble(pair[0]);
                double y = Convert.ToDouble(pair[1]);
                result[j] = new Point(x, y);
                j++;
            }
            return result;
        }

        static void WriteToFile(Point[] data, Point[] clusters, string filenameData, string filenameClusters)
        {
            string dataText = "x;y;cluster_index\n";
            string clusterText = "x;y\n";
    

            for(int i =0; i < data.Length; i++)
            {
                dataText += data[i] + "\n";
            }
            for (int i =0; i < clusters.Length; i++)
            {
                clusterText += clusters[i].X.ToString().Replace(',', '.') + ";" + clusters[i].Y.ToString().Replace(',', '.') + "\n";
            }

            System.IO.File.WriteAllText(filenameData, dataText);
            System.IO.File.WriteAllText(filenameClusters, clusterText);
        }

        static void AssignCluster(ref Point p, ref Point[] clusters)
        {
            int min = 0;
            for(int i =0; i < clusters.Length; i++)
            {
                if (p.Distance(clusters[i]) < p.Distance(clusters[min]))
                {
                    min = i;
                }    
            }
            p.ClusterIndex = min;
        }

        static Point[] RecalculateClusters(Point[] data, int k)
        {
            Point[] newClusters = new Point[k];


            Parallel.For(0, k, i =>
            {
                Point temp = new Point(0, 0);
                int counter = 0;
                for (int j = 0; j < data.Length; j++)
                {
                    if (data[j].ClusterIndex == i)
                    {
                        temp.X += data[j].X;
                        temp.Y += data[j].Y;
                        counter++;
                    }
                }
                temp.X /= counter;
                temp.Y /= counter;
                newClusters[i] = temp;
            });

            return newClusters;
        }

        static Point[] k_means(Point[] data, int k)
        {
            // assign initial clusters
            Point[] clusters = new Point[k];
            for(int i = 0; i < k; i++)
            {
                clusters[i] = data[i];
            }


            bool changed = true;
            while (changed)
            {
                // assign clusters to points
                Parallel.For(0, k, i =>
                {
                    for (int j = 0; j < data.Length / k; j++)
                    {
                        int index = i * (data.Length / k) + j;
                        AssignCluster(ref data[index], ref clusters);
                    }

                    for (int j = 0; j < data.Length % k; j++)
                    {
                        int index = (data.Length / k) * k + j;
                        AssignCluster(ref data[index], ref clusters);
                    }
                });

                //recalculate clusters
                Point[] recalculatedClusters = RecalculateClusters(data, k);
                changed = false;
                for (int i = 0; i < k; i++)
                {
                    if (!(clusters[i].X == recalculatedClusters[i].X && clusters[i].Y == recalculatedClusters[i].Y)) changed = true;
                }
                clusters = recalculatedClusters;
            }

            return clusters;
        }

        static void Main(string[] args)
        {
            int k = 8;
            Point[] data = Program.ReadFile("../../../../../../py/dataset/input.csv");
            Point[] clusters = k_means(data, k);
            WriteToFile(data, clusters, "../../../../../../py/dataset/result_points.csv", "../../../../../../py/dataset/result_clusters.csv");
        }
    }
}
