package io.jenkins.plugins.jobtracker;

import hudson.Extension;
import hudson.model.Action;
import hudson.model.Cause;
import hudson.model.CauseAction;
import hudson.model.Run;
import hudson.model.TaskListener;
import javax.annotation.Nonnull;
import hudson.model.listeners.RunListener;
import hudson.triggers.SCMTrigger;

import java.util.logging.Logger;
import java.io.FileWriter;
import java.io.IOException;
import jenkins.model.Jenkins;

@Extension
public class JobTracker extends RunListener<Run> {
    private static final Logger LOGGER = Logger.getLogger(JobTracker.class.getName());

    @Override
    public void onCompleted(Run run, @Nonnull TaskListener listener) {
        listener.getLogger().println("hahaha");
        log(run, "COMPLETED");
    }

    @Override
    public void onStarted(Run run, TaskListener listener) {
        log(run, "STARTED");
    }

    @Override
    public void onDeleted(Run run) {
        log(run, "DELETED");
    }

    private void log(Run<?, ?> run, String status) {
        String jobName = run.getParent().getDisplayName();
        String timestamp = run.getTimestampString2();
        int buildNumber = run.getNumber();
        String userName = getUserName(run);
        String gitInfo = "nogit";
    
        String message = String.format(
                "Job '%s' %s at %s with build number #%d (User: %s, Git: %s)",
                jobName, status, timestamp, buildNumber, userName, gitInfo);
        writeToAuditLog(message);
    }
    
    private String getUserName(Run<?, ?> run) {
        CauseAction causeAction = run.getAction(CauseAction.class);
        if (causeAction != null) {
            Cause.UserIdCause userIdCause = causeAction.findCause(Cause.UserIdCause.class);
            if (userIdCause != null) {
                return userIdCause.getUserName();
            }
        }
        return "Unknown";
    }

    private void writeToAuditLog(String message) {
        try {
            FileWriter fileWriter = new FileWriter("/tmp/haha");
            fileWriter.write(message);
            fileWriter.close();
        } catch (IOException e) {
            LOGGER.warning("Failed to write to /tmp/haha: " + e.getMessage());
        }
//        Jenkins.getInstanceOrNull().get.println("[Audit Log] " + message);
        LOGGER.info(message);
    }
}
