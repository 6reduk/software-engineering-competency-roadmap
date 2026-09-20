---
id: a3
kind: track
title: Networks, Linux & Security Foundations
status: accepted
updated: 2026-08-15
language: ru
---

# A3 Networks, Linux & Security Foundations

## Mission

Дать рабочую модель среды выполнения и пути запроса, позволяющую диагностировать системные проблемы и принимать базово безопасные решения.

## In scope

Linux runtime, network stack, DNS/TLS/HTTP infrastructure, identity/security foundations и software supply chain baseline.

## Non-goals

Application API design — B2; distributed protocols — B5; Kubernetes/cloud networking, artifact signing/scanning и admission/policy enforcement платформы — B6; SRE operations — B7; security governance — C1. A3 владеет security baseline, threat model и принципами supply-chain trust.

## Clusters

- `a3.cluster.linux-runtime` — процессы, права, signals, files и resource limits.
- `a3.cluster.network-stack` — TCP/IP, UDP, sockets, routing и connection lifecycle.
- `a3.cluster.dns-service-discovery` — DNS и базовые discovery patterns.
- `a3.cluster.tls-pki` — TLS, certificates, PKI и trust boundaries.
- `a3.cluster.http-proxies` — HTTP mechanics, proxies, gateways и load balancers.
- `a3.cluster.identity-access` — authentication, authorization, sessions и tokens.
- `a3.cluster.secrets-crypto-basics` — secrets и прикладные cryptographic boundaries.
- `a3.cluster.threat-modeling-appsec` — threats, common vulnerability classes и secure defaults.
- `a3.cluster.supply-chain-security` — dependencies, artifacts, provenance и vulnerability handling.

## Hard baseline prerequisites

Нет.

## Conditional prerequisites

Нет.

## Strong connections

A2, B2, B5, B6, B7, B11, C1.
