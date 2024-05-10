import { query, mutation } from "./_generated/server"
import { v } from 'convex/values'

interface Job {
  title: string,
  location: string,
  date: string,
  seen: boolean,
}

export const get = query({
  handler: async ({ db }) => {
    return await db.query("jobs").collect();
  },
});

export const getByTitle = query ({
  args: { jobTitle: v.string()},
  handler: async (ctx, args) => {
    const job = await ctx.db.query("jobs").filter((q) => q.eq(q.field("jobTitle"), args.jobTitle)).first();
    return job;
  }
})

export const createJob = mutation({
  args: { jobTitle: v.string(), location: v.string(), date: v.string(), seen: v.boolean() },
  handler: async (ctx, args) => {
    const newJobId = await ctx.db.insert("jobs", 
      {
        jobTitle: args.jobTitle , location: args.location, date: args.date, seen: args.seen
      }
    );
    return newJobId;
  }
})